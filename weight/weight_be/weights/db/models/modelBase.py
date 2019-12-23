#! /usr/bin/env python3

from mysql.connector import errors, errorcode
from functools import partialmethod

from gan_shmuel.weight.weight_be.weights.utils import check_field_in_dict

class ModelBase(object):
    def __init__(self, sub_name:str, **row_dict : dict):
        if self.check_row_schema(row_dict):
            for k,v in row_dict.items():
                self._row_dict = row_dict
                if k not in self.get_readonly_attr_names():
                    setattr(
                        self, k, 
                        property(
                            partialmethod(self.__get_data, key=k),
                            partialmethod(self.__set_data, key=k)
                        )
                    )
                else:
                    setattr(
                        self, k, 
                        property(partialmethod(self.__get_data, key=k))
                    )
        else:
            raise errors.DataError("{} Schema is incorrect!".format(sub_name))

    @staticmethod
    def check_row_schema(**row_dict : dict) -> bool:
        raise NotImplementedError

    @staticmethod
    def get_readonly_attr_names() -> tuple:
        raise NotImplementedError

    def __get_data(self, key:str='', default:any=None) -> any:
        return self._row_dict[key] if key in self._row_dict else default

    def __set_data(self, key:str='', val:any=None):
        if key in self._row_dict:
            self._row_dict[key] = val

    def toDict(self):
        return self._row_dict

    def toTuple(self):
        return tuple(self._row_dict.values())
