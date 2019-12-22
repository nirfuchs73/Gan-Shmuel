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


def create_app(test_config=None):
    s_key = 'dev' if True else token_urlsafe(35)
    my_app = Flask(__name__)
    my_app.config.from_mapping(
        SECRET_KEY=s_key,
        # DATABASE=os.path.join(my_app.instance_path, 'chatr.sqlite'),
        DATABASE_HOST='mysql',
        DATABASE_PORT='3306',
        DATABASE_DATABASE='mysql',
        DATABASE_USER='mysql',
        DATABASE_PASSWORD='mysql',
        # FAKER_JSON=os.path.join(my_app.instance_path, 'weights.json')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        my_app.config.from_pyfile(
            os.path.join(my_app.root_path,'config.py'), 
            silent=True
        )
    else:
        # load the test config if passed in
        my_app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(my_app.instance_path)
    # except OSError:
    #     pass

    
    db.init_app(my_app)

    from . import bp
    my_app.register_blueprint(bp.create_views_blueprint())

    return my_app
