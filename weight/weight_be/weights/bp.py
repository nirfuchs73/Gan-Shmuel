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
    format_dt, get_dt, allowed_file, get_file_ext
)

from flask import (
    Blueprint, flash, g, redirect, 
    render_template, request, session, url_for,
    current_app, make_response, jsonify
)

from datetime import datetime, timezone, timedelta

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
        
    @bp.route('/batch-weight', methods=['GET','POST'])
    def batch_weight():
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
        ''' return list id of containers without weight '''
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

    @bp.route('/weight2', methods=['POST'])
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
                if force==False or direction=="none":
                    return BadRequest()
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
                if force==False:
                    return BadRequest()
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

    return bp


