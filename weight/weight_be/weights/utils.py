#! /usr/bin/env python3


from datetime import datetime, timezone
from io import StringIO
# from sys import stdin, stderr, stdout
import sys


def get_dt_format_str():
    return '%Y-%m-%d %H:%M:%S'

def get_dt(as_str=False, format_str=None):
    dt = datetime.now(timezone.utc)
    return format_dt(dt, format_str) if as_str else dt

def format_dt(dt, format_str=None):
    fs = get_dt_format_str() if format_str is None else format_str
    return dt.strftime(fs)

def dbg_format(data,debug=False):
    if debug:
        strm = StringIO(str(type(data)))
        if isinstance(data, (list, tuple)):
            print(len(data), " [", file=strm)
            for i in data:
                print(dbg_format(i, debug), file=strm)
            print("]", file=strm)
        elif isinstance(data, dict):
            print(len(data), " {", file=strm)
            for k,v in data.items():
                print(k, ' : ', dbg_format(v, debug), file=strm)
            print('}', file=strm)
        elif isinstance(data, (int, float, str)):
            print(data, file=strm)
        elif isinstance(data, StringIO):
            print(data.getvalue(), file=strm)
        return strm.getvalue()
    else:
        return ''

def dbg_print(data, debug=False, file=sys.stdout):
    if debug:
        print(dbg_format(data,debug), file=file)
        
def check_field_in_dict(key, arg_dict, val_type):
    return key in arg_dict and \
            isinstance(arg_dict.get(key), val_type)

def get_checked_field_in_dict(key, arg_dict, val_type, default=None):
    res_tmp = val_type() if default is None else default
    if check_field_in_dict(key, arg_dict, val_type):
        return arg_dict.get(key, res_tmp)
    else:
        return res_tmp        
        
        
        # gilads utils

def allowed_file_ext():
    return ('csv','json')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_ext()

def get_file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()
           

