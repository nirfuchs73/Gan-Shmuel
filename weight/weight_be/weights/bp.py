#! /usr/bin/env python3


# global (system) imports
import functools

#add by gilad for batch_weight
import os
import csv
#add by gilad for batch_weight

from flask import (
    Blueprint, flash, g, redirect, 
    render_template, request, session, url_for,
    current_app, make_response, jsonify
)
# from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.utils import secure_filename

from . import db

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
        return jsonify({'message':"Error Checking Database Tables!", 'status':404})

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
   
   

    return bp