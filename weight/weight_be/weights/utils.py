#! /usr/bin/env python3


from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
# from sys import stdin, stderr, stdout
import sys
from flask import current_app, g


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

def get_logger_path(app=current_app):
    log_path = Path(
        app.instance_path, 
        'log-{}-{}.log'.format(app.config.get('SECRET_KEY'), get_dt(True))
    )
    return log_path

def get_logger(app=current_app):
    if 'weight_flask_app_logger' not in g:
        log_path = get_logger_path(app)
        g.weight_flask_app_logger = log_path.open('w')
    return g.weight_flask_app_logger

def write_to_logger(data, to_debug_str=False):
    if to_debug_str:
        dbg_print(data, True, file=get_logger())
    else:
        print(data, file=get_logger())

def check_field_in_dict(key, arg_dict, val_type):
    return key in arg_dict and \
            isinstance(arg_dict.get(key), val_type)

def get_checked_field_in_dict(key, arg_dict, val_type, default=None):
    res_tmp = val_type() if default is None else default
    if check_field_in_dict(key, arg_dict, val_type):
        return arg_dict.get(key, res_tmp)
    else:
        return res_tmp

def build_query_str_from_seq(seq, indxs_as_str=tuple(), as_ps=True):
    query_str = ''
    if isinstance(seq, list) or isinstance(seq, tuple):
        if len(seq) > 0:
            for i in range(0,len(seq)):
                if as_ps:
                    param = "%s," if i not in indxs_as_str else "'%s',"
                    query_str = str().join([query_str, param])
                else:
                    param = "{}," if i not in indxs_as_str else "'{}',"
                    query_str = str().join([query_str, param.format(seq[i])])
            query_str = query_str.rstrip(',')
    elif isinstance(seq, dict):
        if len(seq) > 0:
            for k,v in seq.items():
                if as_ps:
                    param = '%({})s,' if k not in indxs_as_str else "'%({})s',"
                    query_str = str().join([query_str, param.format(k)])
                else:
                    param = '{},' if k not in indxs_as_str else "'{}',"
                    query_str = str().join([query_str, param.format(v)])
            query_str = query_str.rstrip(',')
    else:
        raise TypeError
    return query_str
        
        # gilads utils

def allowed_file_ext():
    return ('csv','json')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_ext()

def get_file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()
           

