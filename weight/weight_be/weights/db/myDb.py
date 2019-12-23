#! /usr/bin/env python3


from mysql.connector import connect, errorcode, Error
from flask import current_app, g
from datetime import datetime, timezone


class MyDb(object):
    def __init__(self, app):
        self.__set_db(app)

    def close(self):
        self.__set_db(current_app)
        self.db.close()

    @staticmethod
    def __get_db(app):
        try:
            db_config = app.config.get_namespace('DATABASE_')
            db_nconfig = {
                'host':      str(db_config['host']),
                'port':      int(db_config['port']),
                'database':  str(db_config['database']),
                'user':      str(db_config['user']),
                'password':  str(db_config['password'])
            }
            return connect(**db_nconfig)
        except Error as e:
            raise
    
    def __set_db(self, app):
        try:
            self.db = self.__get_db(app)
            return self.db
        except Error as e:
            raise
        
    def __get_cursor(self, app):
        try:
            self.__set_db(app)
            # self.cur = self.db.cursor(prepared=True, dictionary=True)
            self.cur = self.db.cursor(dictionary=True)
            return self.cur
        except Error as e:
            raise

    def __check__params(self, params):
        if isinstance(params, list):
            return tuple(params)
        elif isinstance(params, tuple) or isinstance(params, dict):
            return params
        else:
            raise TypeError("Error! Params must be a Tuple, a List or a Dict!")
            

    # def init(app, filename):
    #     self.db = self.__get_db(app)
    #     with app.open_resource(filename) as f:
    #         self.db.executescript(f.read().decode('utf8'))
        
    def show_tables(self):
        query = 'SHOW TABLES'
        cur = self.__get_cursor(current_app)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res

    def describe(self, app, table):
        # describe containers_registered;
        # describe transactions;
        query = "DESCRIBE {}".format(table)
        cur = self.__get_cursor(current_app)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res

    # a few general SQL command execution methods

    def execute(self, query, params=[]):
        cur = self.__get_cursor(current_app)
        try:
            cur.execute(query, self.__check__params(params))
            cur.close()
            return cur.rowcount
        except Error as e:
            raise
        except TypeError as t:
            raise
        

    def execute_and_get_all(self, query, params=[]):
        cur = self.__get_cursor(current_app)
        try:
            cur.execute(query, self.__check__params(params))
            res = cur.fetchall()
            cur.close()
            return res
        except Error as e:
            raise
        except TypeError as t:
            raise

    def execute_and_get_one(self, query, params=[]):
        cur = self.__get_cursor(current_app)
        try:
            cur.execute(query, self.__check__params(params))
            res = cur.fetchone()
            cur.close()
            return res
        except Error as e:
            raise
        except TypeError as t:
            raise
