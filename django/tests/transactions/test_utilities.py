"""
Legacy transaction and coinbase transaction from:
https://bitcoin.org/en/developer-reference#raw-transaction-format
"""
from unittest.case import TestCase

from core.serialization import streamify_if_bytes
from transactions.utilities import (
    parse_input,
    parse_output,
    parse_transaction,
    parse_witness,
)


class TransactionUtilitiesTest(TestCase):
    def test_parse_transaction(self):
        tx_hex = (
            "01000000"  # Version
            "01"  # Number of inputs
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
            "01"  # Number of outputs
            "f0ca052a01000000"  # Satoshis (49.99990000 BTC)
            "19"  # Bytes in pubkey script: 25
            "76"  # OP_DUP
            "a9"  # OP_HASH160
            "14"  # Push 20 bytes as data
            "cbc20a7664f2f69e5355aa427045bc15"
            "e7c6c772"  # PubKey hash
            "88"  # OP_EQUALVERIFY
            "ac"  # OP_CHECKSIG
            "00000000"  # locktime: 0 (a block height)
        )
        tx_bytes = bytes.fromhex(tx_hex)
        tx_bytes = streamify_if_bytes(tx_bytes)
        transaction, inputs, outputs = parse_transaction(tx_bytes)

        self.assertEqual(transaction.version, 1)
        self.assertEqual(transaction.locktime, 0)

        self.assertEqual(len(inputs), 1)
        self.assertEqual(len(outputs), 1)

        for input_ in inputs:
            self.assertIsNone(input_.witness, "no witness for legacy tx")

    def test_parse_input(self):
        """ continuation of test_parse_transaction to increase
        readability and lessen test noise """
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
            "outpoint txid is incorrect",
        )

        self.assertEqual(tx_input.vout, 0, "outpoint index is incorrect")

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
        """ continuation of test_parse_transaction to increase
        readability and lessen test noise """
        output_hex = (
            "f0ca052a01000000"  # Satoshis (49.99990000 BTC)
            "19"  # Bytes in pubkey script: 25
            "76"  # OP_DUP
            "a9"  # OP_HASH160
            "14"  # Push 20 bytes as data
            "cbc20a7664f2f69e5355aa427045bc15"
            "e7c6c772"  # PubKey hash
            "88"  # OP_EQUALVERIFY
            "ac"  # OP_CHECKSIG
        )
        output_bytes = streamify_if_bytes(bytes.fromhex(output_hex))
        tx_output = parse_output(output_bytes, 0)

        self.assertEqual(4999990000, tx_output.value)
        self.assertEqual(
            (
                "76"  # OP_DUP
                "a9"  # OP_HASH160
                "14"  # Push 20 bytes as data
                "cbc20a7664f2f69e5355aa427045bc15"
                "e7c6c772"  # PubKey hash
                "88"  # OP_EQUALVERIFY
                "ac"  # OP_CHECKSIG
            ),
            tx_output.script_pubkey,
        )
        self.assertEqual(tx_output.n, 0)

    def test_parse_coinbase_transaction(self):
        coinbase_tx_hex = (
            "01000000"  # Version
            "01"  # Number of inputs
            "00000000000000000000000000000000"
            "00000000000000000000000000000000"  # Previous outpoint TXID
            "ffffffff"  # Previous outpoint index
            "29"  # Bytes in coinbase
            "03"  # Bytes in height
            "4e0105"  # Height: 328014
            "062f503253482f0472d35454085fffed"
            "f2400000f90f54696d65202620486561"
            "6c74682021"  # Arbitrary data
            "00000000"  # Sequence
            "01"  # Output count
            "2c37449500000000"  # Satoshis (25.04275756 BTC)
            "1976a914a09be8040cbf399926aeb1f4"
            "70c37d1341f3b46588ac"  # P2PKH script
            "00000000"  # Locktime
        )
        coinbase_tx_bytes = bytes.fromhex(coinbase_tx_hex)
        coinbase_tx_bytes = streamify_if_bytes(coinbase_tx_bytes)
        transaction, inputs, outputs = parse_transaction(coinbase_tx_bytes)

        # --------- coinbase-specific asserts ---------- #
        self.assertEqual(len(inputs), 1, "coinbase tx has one input")
        self.assertIsNone(inputs[0].witness, "no witness for coinbase tx")

        coinbase_input = inputs[0]
        self.assertEqual(coinbase_input.txid, "00" * 32, "outpoint txid must be null")
        self.assertEqual(coinbase_input.vout, 2 ** 32 - 1, "outpoint index must be max")
        # ---------------------------------------------- #

        self.assertEqual(len(outputs), 1)

        self.assertEqual(transaction.version, 1)
        self.assertEqual(transaction.locktime, 0)

    def test_parse_segwit_transaction(self):
        """
        https://btc-explorer.com/tx/e028625516b04e9652c156c45483779a767e9e8b73da126140e55a53c22cd6ab

        tests/data/segwit_native_3.json
        """
        tx_hex = (
            "01000000000101dca4c43a7ccf697068782784b281b5fc00f9de3e3b8008"
            "70f890505cc1ae1ed10100000000ffffffff03808d5b000000000017a914"
            "c462d9a12ba8739c3080df25d302f49c2326bb2b87501d63020000000019"
            "76a91426ec86b2fbfe054f0a4c8f9f875229bdb570701088ace6eedb1a00"
            "000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b"
            "9fc63d622ff8c58d04004730440220132c0a8e96742ad8fe23bd77fd5646"
            "c8f227baaaa43f0bc84cc610f562bffaa2022071100f27280c36e3421d50"
            "d9be5e87e12cc0f742c2e9a4957ad9773cc776d7d001473044022054e768"
            "d8bbd05ed384a0b362a7bcacd7a4e1c51ce0c758da8d54ef7308af1ac402"
            "205d645e8c96d63819c2759f6de95f6372d8f5d9168a92ea512a304faa28"
            "837a1f016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6"
            "ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8c"
            "ac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee4"
            "5e84a8a48ad05bd8dbb395c011a32cf9f88053ae00000000"
        )
        tx_bytes = bytes.fromhex(tx_hex)
        transaction, inputs, outputs = parse_transaction(tx_bytes)

        self.assertEqual(transaction.version, 1)
        self.assertEqual(transaction.locktime, 0)

        self.assertEqual(len(inputs), 1)
        self.assertEqual(len(outputs), 3)

        input_ = inputs[0]
        self.assertEqual(
            input_.txid,
            "d11eaec15c5090f87008803b3edef900fcb581b2842778687069cf7c3ac4a4dc",
        )
        self.assertEqual(input_.vout, 1)
        self.assertEqual(input_.script_sig, "")
        self.assertEqual(len(input_.witness), 4)

    def test_parse_witness(self):
        """ continuation of 'test_parse_segwit_transaction' but
        separated out for readability and to lessen test noise """
        witness_hex = (
            "04"  # number of stack items
            "00"  # item size
            "47"  # item size
            "30440220132c0a8e96742ad8fe23bd77fd5646c8f227baaaa43f0bc84cc610f56"
            "2bffaa2022071100f27280c36e3421d50d9be5e87e12cc0f742c2e9a4957ad977"
            "3cc776d7d001"
            "47"  # item size
            "3044022054e768d8bbd05ed384a0b362a7bcacd7a4e1c51ce0c758da8d54ef730"
            "8af1ac402205d645e8c96d63819c2759f6de95f6372d8f5d9168a92ea512a304f"
            "aa28837a1f01"
            "69"  # item size
            "52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd929"
            "76b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff0187"
            "4496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c01"
            "1a32cf9f88053ae"
        )
        witness_bytes = bytes.fromhex(witness_hex)
        witness_bytes = streamify_if_bytes(witness_bytes)
        witness_stack_items = parse_witness(witness_bytes)
        self.assertListEqual(
            witness_stack_items,
            [
                bytes.fromhex(""),
                bytes.fromhex(
                    "30440220132c0a8e96742ad8fe23bd77fd5646c8f227baaaa43f0bc8"
                    "4cc610f562bffaa2022071100f27280c36e3421d50d9be5e87e12cc0"
                    "f742c2e9a4957ad9773cc776d7d001"
                ),
                bytes.fromhex(
                    "3044022054e768d8bbd05ed384a0b362a7bcacd7a4e1c51ce0c758da"
                    "8d54ef7308af1ac402205d645e8c96d63819c2759f6de95f6372d8f5"
                    "d9168a92ea512a304faa28837a1f01"
                ),
                bytes.fromhex(
                    "52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e"
                    "0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac"
                    "749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fe"
                    "e45e84a8a48ad05bd8dbb395c011a32cf9f88053ae"
                ),
            ],
        )
