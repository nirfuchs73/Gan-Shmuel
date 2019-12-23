#! /usr/bin/env python3

from . import modelBase

class Container(modelBase.ModelBase):
    def __init__(self, **row_dict : dict):
        super().__init__('Container', row_dict=row_dict)

    @staticmethod
    def check_row_schema(**row_dict : dict) -> bool:
        if "container_id" in row_dict and \
            isinstance(row_dict["container_id"], str) and \
            "weight" in row_dict and \
            isinstance(row_dict["weight"], int) and \
            "unit" in row_dict and \
            isinstance(row_dict["unit"], str):
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
