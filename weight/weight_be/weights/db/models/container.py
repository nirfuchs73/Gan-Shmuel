#! /usr/bin/env python3

from . import modelBase
from weights import utils

class Container(modelBase.ModelBase):
    def __init__(self, **row_dict : dict):
        super().__init__('Container', row_dict=row_dict)

    @staticmethod
    def check_row_schema(**row_dict : dict) -> bool:
        if utils.check_field_in_dict("container_id", row_dict, str) and \
            utils.check_field_in_dict("weight", row_dict, int) and \
            utils.check_field_in_dict("unit", row_dict, str):
            return True
        else:
            return False

    @staticmethod
    def get_readonly_attr_names() -> tuple:
        return tuple()

    # def toTuple(self):
    #     return tuple(self.id, self.weight, self.unit)

    # def toDict(self):
    #     return {
    #         'container_id' : self.id,
    #         'weight' : self.weight,
    #         'unit' : self.unit
    #     }
