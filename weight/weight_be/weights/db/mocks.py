#! /usr/bin/env python3


from .. import utils
from datetime import datetime, timezone
from faker import Faker
from pathlib import Path
from mysql.connector import errorcode, Error

def get_all_of_key_from_dict(dict_list, key):
    res = []
    for i in dict_list:
        if key in i:
            res.append(i[key])
    return res

def create_mocks(cdb):
    faking = Faker()
    conts = []
    conts_dict = []
    produce_elems = ['Navel', 'Blood', 'Mandarin', 'Shamuti', 'Tangerine', 'Clementine', 'Grapefruit', 'Valencia']
    dir_elems = ['in', 'out', 'none']
    for i in range(0, 10000):
        cstr = "{}-{}".format(faking.random_uppercase_letter(), faking.random_number(digits=5, fix_len=True))
        if cstr not in conts:
            conts.append(cstr)
            w_tmp = faking.random_element(elements=('N', 'N', 'N', 'N', 'N', 'N', None))
            if w_tmp is not None:
                w_tmp = faking.random_number(digits=3, fix_len=True)
            u_tmp = faking.random_element(elements=('kg', None))
            conts_dict.append({'container_id': cstr, 'weight': w_tmp, 'unit': u_tmp})
    for i in conts_dict:
        query = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
        ror = cdb.execute(query, (i['container_id'], i['weight'], i['unit'],))
        if ror < 0:
            raise Error
    cont_lists = [ [] for i in range(0, 100) ]
    for i in range(0, 100):
        beg = 100 * i
        end = beg + 100
        cont_list = conts[beg:end]
        cnt2_list = conts_dict[beg:end]
        ts = faking.date_time_between(start_date="-30y", end_date="now", tzinfo=timezone.utc)
        all_wght = get_all_of_key_from_dict(cnt2_list, 'weight')
        all_unt = get_all_of_key_from_dict(cnt2_list, 'unit')
        trck_weight = faking.random_number(digits=4, fix_len=False)
        if None not in all_wght and None not in all_unt:
            neto_weight = sum(all_wght) 
            bruto_w = neto_weight + trck_weight
        else:
            neto_weight = 'na'
            bruto_w = trck_weight * 2
        d = {
            'datetime': ts,
            'direction': faking.random_element(elements=dir_elems), # in/out/none
            'truck': faking.license_plate(), # licence plate
            'containers' : ','.join(cont_list), # csv string
            'bruto': bruto_w, # the truck weight include the containers -- all full
            'truckTara' : trck_weight, # truck weight without the containers (bruto - neto)
            'neto' : neto_weight, # <int> or "na" // na if some of containers unknown - (sum(all_cont_weights))
            'produce': faking.random_element(elements=produce_elems)
        }
        tq = "INSERT INTO transactions (datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES (%(datetime)s, %(direction)s, %(truck)s, %(containers)s, %(bruto)s, %(truckTara)s, %(neto)s, %(produce)s)"
        ror = cdb.execute(tq, d)
        if ror < 0:
            raise Error
    return 'hello world!'
    
        