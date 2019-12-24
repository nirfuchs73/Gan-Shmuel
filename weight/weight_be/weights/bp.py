#! /usr/bin/env python3

# global (system) imports
import functools

from .utils import (
    check_field_in_dict, get_checked_field_in_dict, 
    format_dt, get_dt
)

from flask import (
    Blueprint, flash, g, redirect, 
    render_template, request, session, url_for,
    current_app, make_response, jsonify
)
from datetime import datetime, timezone, timedelta

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequest

from . import db
from .api.unknown import my_func as get_container_with_no_weight

def create_views_blueprint():
    bp = Blueprint('views', __name__)

    @bp.route('/health', methods=['GET'])
    def health():
        cdb = db.get_db()
        res_t = cdb.show_tables()
        if len(res_t) > 0:
            # check the description of the db tables
            res = cdb.describe(current_app, 'containers_registered')
            if len(res) == 3:
                res = cdb.describe(current_app, 'transactions')
                if len(res) == 9:
                    return jsonify({'message':"OK", 'status':200})
        return jsonify({'message':"Failure", 'status':500})
        
        
    @bp.route('/weight', methods=['GET', 'POST'])
    def weight():
        '''
            POST /weight
                - direction=in/out/none
                - truck=<license> (If weighing a truck. Otherwise "na")
                - containers=str1,str2,... comma delimited list of container ids
                - weight=<int>
                - unit=kg/lbs {precision is ~5kg, so dropping decimal is a non-issue}
                - force=true/false { see logic below }
                - produce=<str> { id of produce, e.g. "orange", "tomato", ... OR "na" if enpty}
                Records data and server date-time and returns a json object with a unique weight.
                Note that "in" & "none" will generate a new session id, and "out" will return session id of previous "in" for the truck.
                "in" followed by "in" OR "out" followed by "out":
                - if force=false will generate an error
                - if force=true will over-write previous weigh of same truck
                "out" without an "in" will generate error
                "none" after "in" will generate error
                Return value on success is:
                { "id": <str>, 
                "truck": <license> or "na",
                "bruto": <int>,
                ONLY for OUT:
                "truckTara": <int>,
                "neto": <int> or "na" // na if some of containers have unknown tara
                }
            GET /weight?from=t1&to=t2&filter=f
                - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
                - f - comma delimited list of directions. default is "in,out,none"
                default t1 is "today at 000000". default t2 is "now". 
                returns an array of json objects, one per weighing (batch NOT included):
                [{ "id": <id>,
                "direction": in/out/none,
                "bruto": <int>, //in kg
                "neto": <int> or "na" // na if some of containers have unknown tara
                "produce": <str>,
                "containers": [ id1, id2, ...]
                },...]
        '''
        errors = []
        try:
            if request.method == 'GET':
                t_td = datetime.today()
                from_str = get_checked_field_in_dict('from', request.args, str) 
                to_str = get_checked_field_in_dict('to', request.args, str)
                filter_str = get_checked_field_in_dict('filter', request.args, str)
                # time format: yyyymmddhhmmss
                time_format = '%Y%m%d%H%M%S'
                if len(from_str) > 0:
                    try:
                        from_dt = datetime.strptime(from_str, time_format)
                    except ValueError as e:
                        raise BadRequest
                else:
                    from_dt = datetime(
                        t_td.year, t_td.month, t_td.day, 
                        0,0,0,0, t_td.tzinfo
                    )
                if len(to_str) > 0:
                    try:
                        to_dt = datetime.strptime(to_str, time_format)
                    except ValueError as e:
                        raise BadRequest
                else:
                    to_dt = get_dt()
                if len(filter_str) > 0:
                    filter_lst = filter_str.split(',')
                else:
                    filter_lst = ['in', 'out', 'none']

            elif request.method == 'POST':
                pass
        except ValueError as e:
            raise BadRequest 
        except BadRequest as e:
            raise
            
    #return list id of containers without weight
    @bp.route('/unknown', methods=['GET'])
    def unknown():
        cdb = db.get_db()
        query="select container_id as id from containers_registered where weight is NULL"
        res = cdb.execute_and_get_all(query)
        return jsonify([ix['id'] for ix in res])
        # return jsonify({'list_id':[ix['id'] for ix in res], 'status':200})
    #    get_container_with_no_weight

    return bp