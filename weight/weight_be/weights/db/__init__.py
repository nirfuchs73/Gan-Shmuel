#! /usr/bin/env python3

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime, timezone


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
    # app.cli.add_command(init_db_command)

# def init_db():
#     db = get_db()
#     db.init(current_app, '')


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# some helper functions:
