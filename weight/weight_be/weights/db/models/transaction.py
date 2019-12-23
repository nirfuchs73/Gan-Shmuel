#! /usr/bin/env python3


from datetime import datetime

from . import modelBase
from gan_shmuel.weight.weight_be.weights.utils import check_field_in_dict

class Transaction(modelBase.ModelBase):
    def __init__(self, **row_dict : dict):
        super().__init__('Transaction', row_dict=row_dict)

    @staticmethod
    def get_readonly_attr_names() -> tuple:
        return ('id',)

    @staticmethod
    def check_row_schema(**row_dict : dict) -> bool:
        if check_field_in_dict('id', row_dict, int) and \
            check_field_in_dict('datetime', row_dict, datetime) and \
            check_field_in_dict('direction', row_dict, str) and \
            check_field_in_dict('truck', row_dict, str) and \
            check_field_in_dict('containers', row_dict, str) and \
            check_field_in_dict('bruto', row_dict, int) and \
            check_field_in_dict('truckTara', row_dict, int) and \
            check_field_in_dict('neto', row_dict, int) and \
            check_field_in_dict('produce', row_dict, str):
            return True
        else:
            return False

    