import traceback
from datetime import date, datetime, time
from decimal import Decimal

from ._imports import json


class _DataEncoder:  # todo: update to use decoder api!
    def __init__(self, data, children=None):
        if children is None:
            self.__children = list()
            self.__first = True
        else:
            self.__children = children
            self.__first = False

        self.target = dict()

        _type = type(data).__name__

        if data is None or data is True or data is False:
            self.target['bool'] = str(data)

        elif isinstance(data, (int, float, str)):
            self.target[_type] = data

        elif isinstance(data, (list, tuple, set)):
            self.target[_type] = list()
            for item in data:
                self.target[_type].append(self.__add(item))

        elif isinstance(data, dict):
            self.target[_type] = dict()

            for key in data:
                _key = self.__add(key)
                _value = self.__add(data[key])
                self.target[_type][_key] = _value

        elif isinstance(data, datetime):
            value = (data.year, data.month, data.day,
                     data.hour, data.minute, data.second, data.microsecond,
                     data.tzinfo)
            value = tuple(x for x in value if x is not None)
            self.target[_type] = self.__add(value)

        elif isinstance(data, date):
            value = data.year, data.month, data.day
            value = tuple(x for x in value if x is not None)
            self.target[_type] = self.__add(value)

        elif isinstance(data, time):
            value = (data.hour, data.minute, data.second, data.microsecond,
                     data.tzinfo)
            value = tuple(x for x in value if x is not None)
            self.target[_type] = self.__add(value)

        elif isinstance(data, Decimal):
            self.target[_type] = self.__add(float(data))

        elif isinstance(data, bytes):
            value = tuple(x for x in data)
            self.target[_type] = self.__add(value)

        else:
            raise TypeError(f'Cannot convert type {type(data)}')

        if not self.__first and self.target not in self.__children:
            self.__children.append(self.target)

    def __add(self, obj):
        target = _DataEncoder(obj, self.__children).target
        return self.__id(self.__children.index(target))

    def __id(self, obj):
        return f'&{obj}'

    def __iter__(self):
        for id, child in enumerate(self.__children):
            yield {self.__id(id): child}
        yield self.target

    def __str__(self):
        return str(self.dict())

    def __repr__(self):
        return repr(self.dict())

    def dict(self):
        values = dict()
        for item in self.__iter__():
            values.update(item)
        return values

    def __json__(self):
        return json.dumps(self.dict())


class Encoder(_DataEncoder):
    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def json(cls, data):
        return cls(data).__json__()
