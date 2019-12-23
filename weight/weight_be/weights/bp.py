#! /usr/bin/env python3

# global (system) imports
import functools

from flask import (
    Blueprint, flash, g, redirect, 
    render_template, request, session, url_for,
    current_app, make_response, jsonify
)
# from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash

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
        return jsonify({'message':"Error Checking Database Tables!", 'status':404})
        
  #return list id of containers without weight
    @bp.route('/unknown', methods=['GET'])
    def unknown():
        cdb = db.get_db()
        query="select container_id as id from containers_registered where weight is NULL"
        res = cdb.execute_and_get_all(query)
        return jsonify({'list_id':[ix['id'] for ix in res], 'status':200})
    #    get_container_with_no_weight

    return bp