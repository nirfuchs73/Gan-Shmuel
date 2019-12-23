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

    @bp.route('/batch-weight', methods=['POST'])
    def batch_weight():
        title = "Batch"
        cdb = db.get_db()
        #dealing with a json/csv file
        jsonFile = "in/containers3.json"
        csvFile = "in/container.csv"
        if os.path.exists(jsonFile):
            file_data = ""
            try:
                with open(jsonFile) as f:
                    file_data = f.read()
                    query = "DELETE * FROM container_registered"
                    cdb.execut(query)
                    query = "INSERT INTO container_registered SELECT * FROM" 
                    cdb.execut(query,[file_data])  
            except:
                return jsonify({'message':"could not read file!", 'status':404})
        elif os.path.exists(csvFile):
            query = "DELETE * FROM container_registered"
            cdb.execut(query)
            file_data = ""
            try:
                with open(csvFile) as f:
                    file_data = f.read().splitlines(True)
                    first_line = file_data[0] 
                    units = first_line.split(',') #we're only intrested in units[1].
                    for line in file_data[1:]:
                        lineSplit = line.split(',')
                        if units[1] == 'kg' or units[1] == 'lbs': #could add functionality for capital letters 
                            query = "INSERT INTO container_registered VALUES (%s, %s, %s);"
                            cdb.execut(query,[lineSplit[0],lineSplit[1], units[1]])
                        else:
                            return jsonify({'message':"no specified data (kg,lbs)", 'status':404})
            except:
                return jsonify({'message':"could not read file!", 'status':404})
        else:
            return jsonify({'message':"found no existing file!", 'status':404})
        #res_t = cdb.show_tables()
   

    return bp