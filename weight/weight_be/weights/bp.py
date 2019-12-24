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

from mysql.connector import errorcode, Error

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequest, InternalServerError

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
        
        
    @bp.route('/weight', methods=['GET'])
    def getWeight():
        errors = []
        try:
            
            t_td = datetime.today()
            from_str = get_checked_field_in_dict('from', request.args, str) 
            to_str = get_checked_field_in_dict('to', request.args, str)
            filter_str = get_checked_field_in_dict('filter', request.args, str)
            # time format: yyyymmddhhmmss
            time_format = '%Y%m%d%H%M%S'
            if len(from_str) > 0:
                from_dt = datetime.strptime(from_str, time_format)
            else:
                from_dt = datetime(
                    t_td.year, t_td.month, t_td.day, 
                    0,0,0,0, t_td.tzinfo
                )
            if len(to_str) > 0:
                to_dt = datetime.strptime(to_str, time_format)
            else:
                to_dt = get_dt()
            if len(filter_str) > 0:
                filter_lst = filter_str.split(',')
            else:
                filter_lst = ['in', 'out', 'none']
            if len(filter_lst) > 0:
                cdb = db.get_db()
                res = []
                query = "SELECT * FROM transactions WHERE datetime BETWEEN %s AND %s AND" 
                q_params = []
                if len(filter_lst) == 1:
                    query = str().join([query, " direction = %s"])
                    q_params.append(filter_lst[0])
                else:
                    query = str().join([query, " direction IN ("])
                    for filter_f in filter_lst:
                        query = str().join([query, "%s,"])
                        q_params.append(filter_f)
                    query = str().join([query.rstrip(','), ")"])
                q_params.extend((from_dt, to_dt,))
                    
                res_sel1 = cdb.execute_and_get_all(query, q_params)
                if len(res_sel1) > 0:
                    for t_trans in res_sel1:
                        trans = db.models.transaction(t_trans)
                        res_d = {
                            'id' : trans.id,
                            "direction": trans.direction,
                            "bruto": trans.bruto, # assuming that bruto is stored as kg..
                            "neto": trans.neto if trans.neto is not None else "na", 
                            "produce": trans.produce,
                            "containers": trans.containers.split(',')
                        }
                        res.append(res_d)
                return jsonify(res)
            else:
                raise BadRequest()
        except Error as e:
            raise InternalServerError()
        except TypeError as e:
            raise InternalServerError()
        except ValueError as e:
            raise BadRequest() 
        except BadRequest as e:
            raise
            
    # return list id of containers without weight
    @bp.route('/unknown', methods=['GET'])
    def unknown():
        cdb = db.get_db()
        query="select container_id as id from containers_registered where weight is NULL"
        res = cdb.execute_and_get_all(query)
        return jsonify([ix['id'] for ix in res])
        # return jsonify({'list_id':[ix['id'] for ix in res], 'status':200})
        # get_container_with_no_weight

    return bp