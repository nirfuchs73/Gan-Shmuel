#! /usr/bin/env python3

# global (system) imports
import functools

#add by gilad for batch_weight
import os
import json
import csv

from csv import DictReader
#add by gilad for batch_weight

from .utils import (
    check_field_in_dict, get_checked_field_in_dict, 
    format_dt, get_dt, build_query_str_from_seq, 
    allowed_file, get_file_ext
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
from werkzeug.utils import secure_filename

from . import db
# from .api.unknown import my_func as get_container_with_no_weight

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
    def get_weight():
        errors = []
        res = []
        query = ''
        neto_query = ''
        conts = []
        try:
            t_td = datetime.today()
            from_str = get_checked_field_in_dict('from', request.args, str) 
            to_str = get_checked_field_in_dict('to', request.args, str)
            filter_str = get_checked_field_in_dict('filter', request.args, str)
            # return jsonify(t_td, from_str, to_str, filter_str)
            # time format: yyyymmddhhmmss
            time_format = '%Y%m%d%H%M%S'
            if len(from_str) > 0:
                from_dt = datetime.strptime(from_str, time_format)
            else:
                from_dt = datetime(t_td.year, t_td.month, t_td.day, 0,0,0,0, t_td.tzinfo)
            if len(to_str) > 0:
                to_dt = datetime.strptime(to_str, time_format)
            else:
                to_dt = get_dt()
            if len(filter_str) > 0:
                filter_lst = filter_str.split(',')
            else:
                filter_lst = ['in', 'out', 'none']
            # return jsonify(t_td, from_dt, to_dt, filter_lst)
            if len(filter_lst) > 0 and '' not in filter_lst:
                cdb = db.get_db()

                # query = "SELECT * FROM transactions AS t WHERE ( t.datetime BETWEEN CAST ( '%s' AS DATETIME ) AND CAST ( '%s' AS DATETIME ) ) AND t.direction IN ( {} );" 
                query = "SELECT * FROM transactions AS t WHERE ( t.datetime BETWEEN CAST( '{}' AS DATETIME ) AND CAST( '{}' AS DATETIME ) ) AND t.direction IN ( {} );" 
                q_params = []
                # q_params.extend([format_dt(from_dt,'%Y-%m-%d %H:%M:%S'), format_dt(to_dt,'%Y-%m-%d %H:%M:%S')])
                # q_params.extend([from_dt, to_dt])
                # if len(filter_lst) == 1:
                #     query = str().join([query, " direction = '%s';"])
                #     q_params.append(filter_lst[0])
                # else:
                # direct = " direction IN ({});".format(build_query_str_from_seq(filter_lst, range(0, len(filter_lst))))
                # query = query.format(from_dt, to_dt, build_query_str_from_seq(filter_lst, range(0, len(filter_lst)), False))
                query = query.format(format_dt(from_dt,'%Y-%m-%d %H:%M:%S'), format_dt(to_dt,'%Y-%m-%d %H:%M:%S'), build_query_str_from_seq(filter_lst, range(0, len(filter_lst)), False))
                # query = str().join([query, direct])
                # q_params.extend(filter_lst)
                # return jsonify(t_td, from_dt, to_dt, filter_lst, q_params, query)
                res_sel1 = cdb.execute_and_get_all(query, q_params)
                # return jsonify(res_sel1)
                if len(res_sel1) > 0:
                    for t_trans in res_sel1:
                        # trans = db.models.transaction(t_trans)
                        neto_res = t_trans.get('neto')
                        t_conts = t_trans.get('containers')
                        if len(t_conts) > 0 :
                            conts_t = t_conts.split(',')
                            if len(conts_t) > 0 and '' not in conts_t:
                                conts.extend(conts_t)
                                conts_qs = build_query_str_from_seq(conts, range(0, len(conts)), False)
                                # conts_qs = build_query_str_from_seq(conts, range(0, len(conts)), True)
                                neto_query = "SELECT * FROM containers_registered WHERE (weight IS NULL OR unit IS NULL) AND container_id IN ({})".format(conts_qs)
                                # neto_lst = cdb.execute_and_get_all(neto_query, conts)
                                neto_lst = cdb.execute_and_get_all(neto_query)
                                neto_res = neto_res if neto_res is not None and neto_res != 0 and len(neto_lst) == 0 else 'na'
                        res_d = {
                            'id' : t_trans.get('id'),
                            "direction": t_trans.get('direction'),
                            "bruto": t_trans.get('bruto'), # assuming that bruto is stored as kg..
                            "neto": neto_res, 
                            "produce": t_trans.get('produce'),
                            "containers": conts
                        }
                        res.append(res_d)
            # else:
            #     raise BadRequest()
        except Error as e:
            return jsonify(str(type(e)), str(e), query, neto_query, conts) # raise InternalServerError()
        except TypeError as e:
            return jsonify(str(type(e)), str(e), query, neto_query, conts) # raise InternalServerError()
        except ValueError as e:
            return jsonify(str(type(e)), str(e), query, neto_query, conts) # raise BadRequest() 
        except BadRequest as e:
            return jsonify(str(type(e)), str(e), query, neto_query, conts) # raise
        return jsonify(res, "OK", query, neto_query, conts)
            
    # return list id of containers without weight
        
    @bp.route('/batch-weight', methods=['GET','POST'])
    def batch_weight():
        #fost a csv/json file to a table in the database
        cdb = db.get_db()
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file
            # browser also submit an empty part without filename 
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename): 
                in_folder = current_app.config.get("UPLOAD_FOLDER")#see config for upload folder
                filename = secure_filename(file.filename)
                filepath = os.path.join(in_folder, filename)
                file.save(filepath)
                query = "DELETE FROM containers_registered"
                cdb.execute(query)
                if get_file_ext(filename) == 'json':
                    try:
                        with open(filepath, 'r') as f:
                            data=json.load(f)
                            for line in data:
                                id = line['id']
                                weight = line['weight']
                                unit = line['unit']
                                query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)" 
                                cdb.execute(query,[id, weight, unit])  
                    except:
                        return jsonify({'message':"could not read file!", 'status':404})
                elif get_file_ext(filename) == 'csv':
                    try:
                        with open(filepath,'r') as f:
                            data = csv.DictReader(f)
                            headers = data.fieldnames # we're only intrested in the units
                            if not headers[1] == 'kg' and not headers[1] == 'lbs':
                                return jsonify({'message':"no specified units (kg,lbs)", 'status':404})
                            for line in data:
                                id = line['id']
                                weight = line[headers[1]] #the lines in data with the kg/lbs header
                                query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)"
                                cdb.execute(query,[id,weight, headers[1]])                        
                    except:
                        return jsonify({'message':"could not read file!", 'status':404})
                else:
                    return jsonify({'message':"found no existing file!", 'status':404})
        return render_template('batch_weight.html.j2')


    @bp.route('/unknown', methods=['GET'])
    def unknown():
        cdb = db.get_db()
        query="select container_id as id from containers_registered where weight is NULL"
        res = cdb.execute_and_get_all(query)
        return jsonify([ix['id'] for ix in res])
        # return jsonify({'list_id':[ix['id'] for ix in res], 'status':200})
    #    get_container_with_no_weight
   

    @bp.route('/session/<id>', methods=['GET'])
    def session(id):
        cdb = db.get_db()
        query="select * from transactions where id={}".format(id)
        res = cdb.execute_and_get_one(query)
        if res == None:
            return jsonify({'message':"session non-existent",'status':404})
        
        res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto']})
        #ONLY for OUT:
        if res['direction']=="out":
            res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto'],"truckTara":res['truckTara'],"neto":res['neto']})

        return res_json


    @bp.route('/item/<id>?from=t1&to=t2', methods=['GET'])
    def item():
        #return info of a container or truck with in defined period
        cdb = db.get_db()
        query="select container_id as id from containers_registered where weight is NULL"
        res = cdb.execute_and_get_all(query)
        return jsonify([ix['id'] for ix in res])


    return bp