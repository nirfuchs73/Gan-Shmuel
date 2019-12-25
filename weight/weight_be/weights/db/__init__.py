#! /usr/bin/env python3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from . import myDb, models, mocks
from .. import utils

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
    app.cli.add_command(init_mock_db_command)
   
def init_mock_db():
    db = get_db()
    mocks.create_mocks(db)

@click.command('init-mock-db')
@with_appcontext
def init_mock_db_command():
    """Clear the existing data and create new (Mock) tables."""
    click.echo('CREATING the Mock Database.')
    init_mock_db()
    click.echo('Initialized the Mock Database.')
