import hashlib


def hash256(byte_stream):
    return hashlib.sha256(hashlib.sha256(byte_stream).digest()).digest()
