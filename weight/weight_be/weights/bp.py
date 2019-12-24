#! /usr/bin/env python3

# global (system) imports
import functools

#add by gilad for batch_weight
import os
#add by gilad for batch_weight

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
        title = "Batch"
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
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                query = "DELETE * FROM container_registered"
                cdb.execute(query)
                file_data = ""
                if get_file_ext(filename) == 'json':
                    try:
                        with open(UPLOAD_FOLDER + filename,'r') as f:
                            file_data = f.read().splitlines(True)
                            #get the data from the json file
                            for line in file_data[1:-1]:
                                fild1,fild2,fild3 = line.split(',')
                                id = fild1.split(':')[1]
                                weight = fild2.split(':')[1]
                                prep_for_unit = fild3.split(':')[1]
                                unit = prep_for_unit.split('}')[0]
                            #now we got id, weight and unit arguments to insert
                            query = "INSERT INTO container_registered VALUES (%s, %s, %s);" 
                            cdb.execute(query,[id, weight, unit])  
                    except:
                        return jsonify({'message':"could not read file!", 'status':404})
                elif get_file_ext(filename) == 'csv':
                    try:
                        with open(UPLOAD_FOLDER + filename,'r') as f:
                            file_data = f.read().splitlines(True)
                            first_line = file_data[0] 
                            units = first_line.split(',') #we're only intrested in units[1].
                            for line in file_data[1:]:
                                lineSplit = line.split(',')
                                if units[1] == 'kg' or units[1] == 'lbs': #could add functionality for capital letters 
                                    query = "INSERT INTO container_registered VALUES (%s, %s, %s);"
                                    cdb.execute(query,[lineSplit[0],lineSplit[1], units[1]])
                                else:
                                    return jsonify({'message':"no specified data (kg,lbs)", 'status':404})
                    except:
                        return jsonify({'message':"could not read file!", 'status':404})
                else:
                    return jsonify({'message':"found no existing file!", 'status':404})
                #res_t = cdb.show_tables()
          return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


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
        if res == None:
            return jsonify({'message':"session non-existent",'status':404})
        
        res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto']})
        #ONLY for OUT:
        if res['direction']=="out":
            res_json=jsonify({"id":res['id'],"truck":res['truck'],"bruto":res['bruto'],"truckTara":res['truckTara'],"neto":res['neto']})

        return res_json

    return bp