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

    def commit(self):
        self.__set_db(current_app)
        self.db.commit()

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

    # def init(app, filename):
    #     self.db = self.__get_db(app)
    #     with app.open_resource(filename) as f:
    #         self.db.executescript(f.read().decode('utf8'))
        
    def show_tables(self):
        '''Retrieves a list of all tables in the database.'''
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
        '''
            Run a non-"Select" or other Data Retrival Query with optional parameters.
            usage: 
            'cdb.execute("<some_query_string_>", [<some_list_or_tuple_of_parameters>])'
            Use "%s" in the query string where you want execute() to insert a parameter
            if using a list or tuple for "params" 
            (Note: it will insert them in the order they are passed into "params"!);
            if using a dict for "params", use "%(<param_key>)s" 
            where "<param_key>" is a key in the dict.
            Parameter "params" MUST be a list , a tuple or a dict!
            Throws a TypeError if "params" is not of the right type!
            Returns the number of Rows "affected" / "inserted" on success.
            Returns -1 (or None) on failure or if unable to determine the number
            of Rows "affected" / "inserted".
            Throws a mysql.connector.errors.Error on internal MySQL Error.
        '''
        cur = self.__get_cursor(current_app)
        try:
            cur.execute(query, self.__check__params(params))
            res = cur.rowcount
            cur.close()
            self.commit()
            return res
        except Error as e:
            raise
        except TypeError as t:
            raise
        

    def execute_and_get_all(self, query, params=[]):
        '''
            Run a "Select" or other Data Retrival Query with optional parameters
            and retrieve ALL results.
            usage: 
            'cdb.execute_and_get_all("<some_query_string_>", [<some_list_or_tuple_of_parameters>])'
            Use "%s" in the query string where you want execute() to insert a parameter
            if using a list or tuple for "params" 
            (Note: it will insert them in the order they are passed into "params"!);
            if using a dict for "params", use "%(<param_key>)s" 
            where "<param_key>" is a key in the dict.
            Parameter "params" MUST be a list , a tuple or a dict!
            Throws a TypeError if "params" is not of the right type!
            Returns a list of all Rows (each as a dict) on success.
            Returns an empty list on failure.
            Throws a mysql.connector.errors.Error on internal MySQL Error.
        '''
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
        '''
            Run a "Select" or other Data Retrival Query with optional parameters
            and retrieve JUST ONE result.
            usage: 
            'cdb.execute_and_get_one("<some_query_string_>", [<some_list_or_tuple_of_parameters>])'
            Use "%s" in the query string where you want execute() to insert a parameter
            if using a list or tuple for "params" 
            (Note: it will insert them in the order they are passed into "params"!);
            if using a dict for "params", use "%(<param_key>)s" 
            where "<param_key>" is a key in the dict.
            Parameter "params" MUST be a list , a tuple or a dict!
            Throws a TypeError if "params" is not of the right type!
            Returns the Row (as a dict) on success.
            Returns None on failure.
            Throws a mysql.connector.errors.Error on internal MySQL Error.
        '''
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
