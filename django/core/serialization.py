import logging
from io import BytesIO


logger = logging.getLogger(__name__)


class SerializationError(RuntimeError):
    pass


def encode_as_varint(x):
    """
    https://bitcoin.org/en/developer-reference#compactsize-unsigned-integers
    """
    if 0 <= x <= 252:
        return x.to_bytes(1, 'little')
    elif 253 <= x <= 0xffff:
        return b'\xfd' + x.to_bytes(2, 'little')
    elif 0x10000 <= x <= 0xffffffff:
        return b'\xfe' + x.to_bytes(4, 'little')
    elif 0x100000000 <= x <= 0xffffffffffffffff:
        return b'\xff' + x.to_bytes(8, 'little')
    else:
        raise SerializationError(f'integer is out of range: {x}')


def decode_varint(byte_stream):
    byte_stream = streamify_if_bytes(byte_stream)

    x = byte_stream.read(1)[0]

    if 0 <= x <= 252:
        return x

    if x == 253:
        int_bytes = byte_stream.read(2)
    elif x == 254:
        int_bytes = byte_stream.read(4)
    elif x == 255:
        int_bytes = byte_stream.read(8)
    else:
        raise Exception()

    return int.from_bytes(int_bytes, 'little')


def streamify_if_bytes(byte_stream):
    if isinstance(byte_stream, bytes):
        byte_stream = BytesIO(byte_stream)

    return byte_stream
