from unittest.case import TestCase

from core.serialization import streamify_if_bytes
from transactions.utilities import parse_input


"""
https://bitcoin.org/en/developer-reference#raw-transaction-format


################################################
##### Transaction: spend p2pk, pay p2pkh #######
################################################



01000000 ................................... Version

01 ......................................... Number of inputs
|
| 7b1eabe0209b1fe794124575ef807057
| c77ada2138ae4fa8d6c4de0398a14f3f ......... Outpoint TXID
| 00000000 ................................. Outpoint index number
|
| 49 ....................................... Bytes in sig. script: 73
| | 48 ..................................... Push 72 bytes as data
| | | 30450221008949f0cb400094ad2b5eb3
| | | 99d59d01c14d73d8fe6e96df1a7150de
| | | b388ab8935022079656090d7f6bac4c9
| | | a94e0aad311a4268e082a725f8aeae05
| | | 73fb12ff866a5f01 ..................... Secp256k1 signature
|
| ffffffff ................................. Sequence number: UINT32_MAX

01 ......................................... Number of outputs
| f0ca052a01000000 ......................... Satoshis (49.99990000 BTC)
|
| 19 ....................................... Bytes in pubkey script: 25
| | 76 ..................................... OP_DUP
| | a9 ..................................... OP_HASH160
| | 14 ..................................... Push 20 bytes as data
| | | cbc20a7664f2f69e5355aa427045bc15
| | | e7c6c772 ............................. PubKey hash
| | 88 ..................................... OP_EQUALVERIFY
| | ac ..................................... OP_CHECKSIG

00000000 ................................... locktime: 0 (a block height)




####################################
##### Coinbase transaction #########
####################################


01000000 .............................. Version

01 .................................... Number of inputs
| 00000000000000000000000000000000
| 00000000000000000000000000000000 ...  Previous outpoint TXID
| ffffffff ............................ Previous outpoint index
|
| 29 .................................. Bytes in coinbase
| |
| | 03 ................................ Bytes in height
| | | 4e0105 .......................... Height: 328014
| |
| | 062f503253482f0472d35454085fffed
| | f2400000f90f54696d65202620486561
| | 6c74682021 ........................ Arbitrary data
| 00000000 ............................ Sequence

01 .................................... Output count
| 2c37449500000000 .................... Satoshis (25.04275756 BTC)
| 1976a914a09be8040cbf399926aeb1f4
| 70c37d1341f3b46588ac ................ P2PKH script
| 00000000 ............................ Locktime
"""


class TransactionUtilitiesTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        input_hex = (
            "7b1eabe0209b1fe794124575ef807057"
            "c77ada2138ae4fa8d6c4de0398a14f3f"  # Outpoint TXID
            "00000000"  # Outpoint index number
            "49"  # Bytes in sig. script: 73
            "48"  # Push 72 bytes as data
            "30450221008949f0cb400094ad2b5eb3"
            "99d59d01c14d73d8fe6e96df1a7150de"
            "b388ab8935022079656090d7f6bac4c9"
            "a94e0aad311a4268e082a725f8aeae05"
            "73fb12ff866a5f01"  # Secp256k1 signature
            "ffffffff"  # Sequence number: UINT32_MAX
        )
        input_bytes = streamify_if_bytes(bytes.fromhex(input_hex))
        tx_input = parse_input(input_bytes)
        self.assertEqual(
            bytes.fromhex(
                "7b1eabe0209b1fe794124575ef807057"
                "c77ada2138ae4fa8d6c4de0398a14f3f"  # Outpoint TXID
            )[::-1].hex(),
            tx_input.txid,
        )

        self.assertEqual(tx_input.vout, 0)

        self.assertEqual(
            (
                "48"  # Push 72 bytes as data
                "30450221008949f0cb400094ad2b5eb3"
                "99d59d01c14d73d8fe6e96df1a7150de"
                "b388ab8935022079656090d7f6bac4c9"
                "a94e0aad311a4268e082a725f8aeae05"
                "73fb12ff866a5f01"  # Secp256k1 signature
            ),
            tx_input.script_sig,
        )

        self.assertEqual(
            int.from_bytes(bytes.fromhex("ffffffff"), "little"), tx_input.sequence
        )

    def test_parse_output(self):
        ...

    def test_parse_witness(self):
        ...

    def test_parse_transaction(self):
        ...
