import traceback
from datetime import date, datetime, time
from decimal import Decimal
from collections import UserDict

from ._imports import json


class _Decoders(UserDict):
    def __init__(self):
        super().__init__({str(x): x for x in (None, True, False)})

        for _type in (bytes ,str ,int, float, dict, list, tuple, set, datetime, date, time, Decimal):
            self.data[_type.__name__] = _type

    def __call__(self, key):
        return self.data[key]


class _DataDecoder:
    def __init__(self, data, children=None):
        if children is None:
            self.__children = dict()
            self.__first = True
        else:
            self.__children = children
            self.__first = False

        self.__target = type

        for key in data:
            if key == 'bool':
                self.__target = _decoder[data[key]]

            elif '&' in key or key in _decoder:
                continue

            else:
                raise ValueError(f'Unknown type {key}, {type(key)}')

        loop = True

        while loop:
            loop = False

            for key in data:
                if '&' in key:
                    try:
                        if key not in self.__children:
                            self.__children[key] = _DataDecoder(data[key], self.__children)()
                    except:
                        loop = True

        for key in data:
            if '&' in key or key == 'bool':
                continue
            elif key in _decoder:
                self.__decode(_decoder(key), data[key])

    def __decode(self, typed, obj):
        if typed in (int, float, str):
            self.__target = typed(obj)

        elif typed in (list, tuple, set):
            target = list()
            for item in obj:
                target.append(self.__children[item])
            self.__target = typed(target)

        elif typed is dict:
            self.__target = dict()
            for key in obj:
                self.__target[self.__children[key]] = self.__children[obj[key]]

        elif typed in (datetime, date, time):
            self.__target = typed(*self.__children[obj])

        elif typed is Decimal:
            self.__target = Decimal(self.__children[obj])

        elif typed is bytes:
            self.__target = bytes(self.__children[obj])

    def __call__(self):
        return self.__target


class Decoder(_DataDecoder):
    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def json(cls, data):
        return cls(json.loads(data))()  # Don't bitch, if you think you can do better, do it!


_decoder = _Decoders()
