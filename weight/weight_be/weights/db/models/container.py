#! /usr/bin/env python3

from mysql.connector import errors, errorcode

class Container(object):
    def __init__(self, **row_dict : dict):
        if self.check_row_schema(row_dict):
            self._container_id = row_dict['container_id']
            self._weight = row_dict['weight']
            self._unit = row_dict['unit']
        else:
            raise errors.DataError("Container Schema is incorrect!")

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

    @property
    def id(self) -> str:
        return self._container_id

    @id.setter
    def id(self, val : str):
        self._container_id = val

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, val : int):
        self._weight = val

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, val : str):
        self._unit = val

    def toTuple(self):
        return tuple(self.id, self.weight, self.unit)

    def toDict(self):
        return {
            'container_id' : self.id,
            'weight' : self.weight,
            'unit' : self.unit
        }
