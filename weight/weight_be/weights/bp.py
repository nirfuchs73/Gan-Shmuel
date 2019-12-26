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
    format_dt, get_dt, allowed_file, get_file_ext,
    get_dt_format_str,build_query_str_from_seq
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

from . import db, utils
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
        # return jsonify(res, "OK", query, neto_query, conts)
        return jsonify(res)
        
    # return list id of containers without weight
        
    @bp.route('/batch-weight', methods=['GET','POST'])
    def batch_weight():
        #post a csv/json file to a table in the database
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
                if get_file_ext(filename) == 'json':
                    try:
                        with open(filepath, 'r') as f:
                            data=json.load(f)
                            for line in data:
                                id = line['id']
                                weight = line['weight']
                                unit = line['unit']
                                #try:
                                query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s);"
                                cdb.execute(query,[id, weight, unit])  
                                #except:
                                #query = "UPDATE containers_registered SET weight = %s , unit = '%s' WHERE container_id = '%s'"
                                #Scdb.execute(query,[weight, unit, id])
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
                                #try:
                                query = "INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)"
                                cdb.execute(query,[id, weight, headers[1]])
                                #except:
                                    #try:
                                        #query = "UPDATE containers_registered SET weight = %s , unit = '%s' WHERE container_id = '%s'"
                                        #cdb.execute(query,[weight, headers[1], id])
                                        #cdb.execute("COMMIT")
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
        if res is None:
            return jsonify({'message':"session non-existent",'status':404})
        
        res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto']})
        #ONLY for OUT:
        if res['direction']=="out":
            res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto'],"truckTara":res['truckTara'],"neto":res['neto']})

        return res_json


    def calculate_neto(bruto,trackTara,list_containers):
        sum_containers=0
        list_containers=list_containers.split(',')
        cdb = db.get_db()
        for item in list_containers:
            query="select * from containers_registered where container_id={}".format(item)
            res = cdb.execute_and_get_one(query)
            if res == None:
                return None
            if res["weight"]==None:
                return None
            if res["unit"]=="lbs":
                sum_containers+= float(res["weight"])*float(0.453592)
            else:
                sum_containers+=float(res["weight"])
        return float(bruto)-float(trackTara)-float(sum_containers)

    @bp.route('/weight', methods=['POST'])
    def weightPost():
        #get data from body
        direction=request.form.get('direction',"none")
        containers=request.form.get('containers')
        truck=request.form.get('truck')
        weight=request.form.get('weight')
        unit=request.form.get('unit')
        produce=request.form.get('produce')
        produce.replace('"', '')
        if (direction=="in" or direction=="none") and containers is None:
            return BadRequest("in/none must get list containers")
        if (direction=="in" or direction=="none") and produce is None:
            return BadRequest("in/none must get produce")
        if truck is None or weight is None or unit is None:
            return BadRequest("error parameters send data by form with values:truck, weight, unit")
        force=request.form.get('force',False)
        weight=float(weight)
        if unit=="lbs":
            weight=(weight*float(0.453592))
        date_session=utils.format_dt(datetime.now(),"%Y-%m-%d %H:%M:%S")
        # return "hi".format(direction)

        #get last session to this truck:
        cdb = db.get_db()

        query="select max(id) as id from transactions where truck={} group by truck".format(truck)
        id_last_session = cdb.execute_and_get_all(query)
        if id_last_session != []:
            id_last_session=id_last_session[0]['id']
            query="select * from transactions where id={}".format(id_last_session)
            last_session = cdb.execute_and_get_all(query)[0]
        else:
            last_session=None


        #in
        if direction=="in" or direction=="none":
            if last_session is None or last_session["direction"]=="out":
                #insert new transaction inneto
                query="insert into transactions (direction,datetime,truck,containers,bruto,produce) values ('{}','{}','{}','{}',{},'{}');‏".format(direction,date_session,truck,containers,weight,produce)
                try:
                    cdb.execute(query)
                except:
                    a="a"

            elif last_session["direction"]=="in" or last_session["direction"]=="none":
                if force== 'False' or direction=="none":
                    return BadRequest("in can't arrive after in or none. for update send force=True")
                else:
                    #update last row in
                    query="update transactions set direction='{}', datetime='{}',truck='{}', containers='{}', bruto={}, produce='{}' where id={};".format(direction,date_session,truck,containers,weight,produce,id_last_session)
                    cdb.execute(query)

        #out
        elif direction=="out":
            if last_session is None:
                return BadRequest("there is no transaction to this truck")
            #calaulate neto
            neto=calculate_neto(last_session["bruto"],weight,last_session["containers"])

            if last_session["direction"]=="out":
                if force == 'False':
                    return BadRequest("out cant arrive after out. for update send force=True")
                else:
                    #update last row out
                    query="update transactions set datetime='{}',truckTara={},neto={},produce='{}' where id={};".format(date_session,weight,neto,produce,last_session["id"])
                    res = cdb.execute(query)
            else:
                #insert new row out
                if produce is None:
                    produce=last_session["produce"]
                query="insert into transactions (direction,datetime,truck,containers,bruto,truckTara,neto,produce) values ('{}','{}','{}','{}',{},{},{},'{}');‏".format(direction,date_session,last_session["truck"],last_session["containers"],last_session["bruto"],weight,neto,produce)
                try:
                    cdb.execute(query)
                except:
                    a="a"

        #return result from db:
        query="select max(id) as id from transactions where truck={} group by truck".format(truck)
        id_last_session = cdb.execute_and_get_all(query)[0]['id']
        #get details:
        query="select * from transactions where id={}".format(id_last_session)
        res = cdb.execute_and_get_one(query)
        if res == None:
            return jsonify({'message':"session non-existent",'status':404})
        res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto']})
        #ONLY for OUT:
        if res['direction']=="out":
            res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto'],"truckTara":res['truckTara'],"neto":res['neto']})
        return res_json


    @bp.route('/item/<id>', methods=['GET'])
    def item(id):
        cdb = db.get_db()
        list_sessions=[]
        date_now=datetime.now()
    
        t1 = request.args.get('from', datetime(date_now.year,date_now.month,1,0,0,0),type = str)
        t2 = request.args.get('to',default = date_now,type = str)

        #convert str to datetime:
        if type(t1) ==str:
            if len(t1)!= 14:
                return BadRequest("date isn't in the format yyyymmddhhmmss")
            t1 = datetime(int(t1[0:4]),int(t1[4:6]),int(t1[6:8]),int(t1[8:10]),int(t1[10:12]),int(t1[12:14]))
        if type(t2) ==str:
            if len(t2)!= 14:
                return BadRequest("date isn't in the format yyyymmddhhmmss")
            t2 = datetime(int(t2[0:4]),int(t2[4:6]),int(t2[6:8]),int(t2[8:10]),int(t2[10:12]),int(t2[12:14]))

        #list transactions
        query="select * from transactions where datetime>='{}' and datetime<='{}';".format(t1,t2)
        list_transaction = cdb.execute_and_get_all(query)

        #try to find container
        query="select * from containers_registered where container_id='{}';".format(id)
        container_object = cdb.execute_and_get_one(query)
        if container_object is not None:
            for line in list_transaction:
                if id in line['containers'].split(','):
                    list_sessions.append(line['id'])
            return jsonify({'id':id,'tara':container_object['weight'],'session':list_sessions})

        #for truck
        else:
            flag_exist_truck=0
            weight_truck=None
            for line in list_transaction:
                if id == line['truck']:
                    flag_exist_truck=1
                    list_sessions.append(line['id'])
                    if line['truckTara'] != "NULL":
                        weight_truck=line['truckTara']
            if flag_exist_truck==0:
                return BadRequest("id not found")
            else:
                return jsonify({'id':id,'tara':weight_truck,'session':list_sessions})

    return bp


