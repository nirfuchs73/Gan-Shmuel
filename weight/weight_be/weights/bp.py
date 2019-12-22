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

def create_views_blueprint():
    bp = Blueprint('views', __name__)

    @bp.route('/health', methods=['GET'])
    def health():
        cdb = db.get_db()
        res_t = cdb.show_tables()
        if len(res_t) > 0:
            # check the description of the db tables
            return jsonify({'message':"OK", 'status':200})
        else:
            return jsonify({'message':"No Database Tables!", 'status':404})
        

    return bp