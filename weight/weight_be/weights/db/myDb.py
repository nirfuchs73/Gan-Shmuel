#! /usr/bin/env python3


import sqlite3
from flask import current_app, g
from datetime import datetime, timezone


class MyDb(object):
    def __init__(self, app):
        self.__set_db(app)

    def close(self):
        self.__set_db(current_app)
        self.db.close()

    def __get_db(self, app):
        db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
        return db
    
    def __set_db(self, app):
        self.db = self.__get_db(app)
        return self.db

    # def init(app, filename):
    #     self.db = self.__get_db(app)
    #     with app.open_resource(filename) as f:
    #         self.db.executescript(f.read().decode('utf8'))
        
    def show_tables(self):
        self.__set_db(current_app)
        query = 'SHOW TABLES'
        return self.db.execute(query).fetchall()

    def execute_and_get_all(self, query, params=[]):
        self.__set_db(current_app)
        return self.db.execute(query, params).fetchall()

    def execute_and_get_one(self, query, params=[]):
        self.__set_db(current_app)
        try:
            return self.db.execute(query, params).fetchone()
        except Exception as e:
            raise
