"""
JSON-RPC described here:
http://chainquery.com/bitcoin-api/getrawtransaction

Serialization format described here with a detailed example:
https://bitcoin.org/en/developer-reference#raw-transaction-format


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
"""
import logging
from io import BytesIO

from django.db import models

from model_utils.models import TimeStampedModel

from blocks.models import Block
from core.hash_utils import hash256
from core.model_fields import BitcoinField, HexField


logger = logging.getLogger(__name__)


def int_to_varint(x):
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
        raise Exception()


def int_from_varint(byte_stream):
    if isinstance(byte_stream, bytes):
        byte_stream = BytesIO(byte_stream)

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


def parse_block(byte_stream, height):
    if isinstance(byte_stream, bytes):
        byte_stream = BytesIO(byte_stream)

    version = int.from_bytes(byte_stream.read(4), 'little')
    prev_hash = byte_stream.read(32).hex()[::-1]
    merkle_root = byte_stream.read(32).hex()[::-1]
    timestamp = int.from_bytes(byte_stream.read(4), 'little')
    bits = byte_stream.read(4).hex()
    nonce = byte_stream.read(4).hex()

    num_transactions = int_from_varint(byte_stream)

    block, created = Block.objects.get_or_create(
        height=height,
        version=version,
        prev_hash=prev_hash,
        merkle_root=merkle_root,
        timestamp=timestamp,
        bits=bits,
        nonce=nonce,
        num_transactions=num_transactions,
    )
    created_or_skipped = 'created' if created else 'skipped'
    logger.debug(f'block {created_or_skipped} at height {height}')

    transactions = [parse_transaction(byte_stream) for _ in range(num_transactions)]

    for transaction in transactions:
        transaction.block = block
        transaction.save()

    return block


def parse_transaction(byte_stream):
    if isinstance(byte_stream, bytes):
        byte_stream = BytesIO(byte_stream)

    version_bytes = byte_stream.read(4)
    version = int.from_bytes(version_bytes, 'little')

    num_inputs = int_from_varint(byte_stream)
    inputs = [parse_input(byte_stream) for _ in range(num_inputs)]

    num_outputs = int_from_varint(byte_stream)
    outputs = [parse_output(byte_stream) for _ in range(num_outputs)]

    locktime_bytes = byte_stream.read(4)
    locktime = int.from_bytes(locktime_bytes, 'little')

    transaction = Transaction.objects.create(
        version=version,
        locktime=locktime,
    )

    for tx_part in inputs + outputs:
        tx_part.transaction = transaction
        tx_part.save()

    return transaction


def parse_input(byte_stream):
    prev_txid = byte_stream.read(32).hex()[::-1]
    prev_index = int.from_bytes(byte_stream.read(4), 'little')

    tx_input = TransactionInput(
        txid=prev_txid,
        vout=prev_index,
    )
    return tx_input


def parse_output(byte_stream):
    value = int.from_bytes(byte_stream.read(8), 'little')
    len_script_pubkey = int_from_varint(byte_stream)
    script_pubkey = byte_stream.read(len_script_pubkey).hex()

    tx_output = TransactionOutput(
        value=value,
        script_pubkey=script_pubkey,
    )
    return tx_output


class Transaction(TimeStampedModel):

    version = models.PositiveIntegerField(help_text='only version 1 valid in Bitcoin Core')
    locktime = models.PositiveIntegerField()

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.PROTECT,
        null=True,
    )

    @property
    def txid(self):
        return hash256(self.serialize())

    def serialize(self):
        raw_tx = b''
        raw_tx += self.version.to_bytes(4, 'little')
        raw_tx += int_to_varint(len(self.vin))
        for input in self.vin:
            raw_tx += input.serialize()
        raw_tx += int_to_varint(len(self.vout))
        for output in self.vout:
            raw_tx += output.serialize()
        raw_tx += self.locktime.to_bytes(4, 'little')
        return raw_tx


class TransactionInput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vin',
        on_delete=models.CASCADE,
    )

    txid = HexField(max_length=64, help_text='transaction hash in hex (32 bytes)')
    vout = models.PositiveIntegerField()

    sequence = models.BigIntegerField()

    script_sig = HexField(max_length=20000)


class TransactionOutput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vout',
        on_delete=models.CASCADE,
    )

    value = BitcoinField()
    n = models.PositiveIntegerField()

    script_pubkey = HexField(max_length=20000)
