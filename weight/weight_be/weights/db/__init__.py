#! /usr/bin/env python3

from flask import current_app, g

from . import myDb

def get_db():
    if 'db' not in g:
        g.db = myDb.MyDb(current_app)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
   
