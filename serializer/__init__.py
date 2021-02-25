from ._encoder import Encoder
from ._decoder import Decoder


def dump(obj):
    return Encoder.json(obj)


def load(obj):
    return Decoder.json(obj)
