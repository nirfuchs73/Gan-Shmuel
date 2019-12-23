#! /usr/bin/env python3


# global (system) imports
from flask import Flask, request, json, url_for
from flask import current_app, render_template, redirect
from secrets import token_urlsafe
import os
from io import StringIO
from datetime import datetime, timezone

# internal (module) imports
from . import db
from . import utils


def create_app(
    host='weight_db', port='3306', 
    database='weight', 
    user='dodo', password='1111', 
    gen_s_key=False, config_file=None
        ):
    debug = True
    
    s_key = token_urlsafe(35) if gen_s_key else 'dev'
    my_app = Flask(__name__)
    my_app.config.from_mapping(
        SECRET_KEY=s_key,
        DATABASE_HOST=host,
        DATABASE_PORT=port,
        DATABASE_DATABASE=database,
        DATABASE_USER=user,
        DATABASE_PASSWORD=password
    )

    utils.dbg_print(my_app.config, debug)

    if config_file is None:
        # load the instance config, if it exists, when not testing
        my_app.config.from_pyfile(
            os.path.join(my_app.root_path,'config.py'), 
            silent=True
        )
        utils.dbg_print(my_app.config, debug)

    else:
        # load the test config if passed in
        my_app.config.from_mapping(config_file)
        

    
    db.init_app(my_app)

    from . import bp
    my_app.register_blueprint(bp.create_views_blueprint())

    return my_app
