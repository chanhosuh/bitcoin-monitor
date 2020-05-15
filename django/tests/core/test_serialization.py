from unittest import TestCase

from core.serialization import SerializationError, decode_varint, encode_as_varint


class VarIntTest(TestCase):
    def test_varint_encoding(self):
        self.assertEqual(encode_as_varint(42), b"*")
        self.assertEqual(encode_as_varint(253), b"\xfd\xfd\x00")
        self.assertEqual(encode_as_varint(255), b"\xfd\xff\x00")
        self.assertEqual(encode_as_varint(0x10000), b"\xfe\x00\x00\x01\x00")
        self.assertEqual(encode_as_varint(0x10010), b"\xfe\x10\x00\x01\x00")

        self.assertEqual(decode_varint(encode_as_varint(42)), 42)
        self.assertEqual(decode_varint(encode_as_varint(253)), 253)
        self.assertEqual(decode_varint(encode_as_varint(561)), 561)
        self.assertEqual(decode_varint(encode_as_varint(12345)), 12345)
        self.assertEqual(decode_varint(encode_as_varint(123456789)), 123456789)
        self.assertEqual(
            decode_varint(encode_as_varint(12345678900000)), 12345678900000
        )

        with self.assertRaises(SerializationError):
            encode_as_varint(0xFFFFFFFFFFFFFFFF + 1)
