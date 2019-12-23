#! /usr/bin/env python3


from datetime import datetime, timezone
from io import StringIO
# from sys import stdin, stderr, stdout
import sys


def get_dt_format_str():
    return '%Y-%m-%d %H:%M:%S'

def get_dt(as_str=False):
    dt = datetime.now(timezone.utc)
    return format_dt(dt) if as_str else dt

def format_dt(dt):
    return dt.strftime(get_dt_format_str())

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

