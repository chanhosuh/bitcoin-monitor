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

from django.db import models
from django.db.models.fields import BigIntegerField

from model_utils.models import TimeStampedModel

from core.hash_utils import hash256
from core.model_fields import HexField
from core.serialization import encode_as_varint


logger = logging.getLogger(__name__)


class Transaction(TimeStampedModel):

    txid = HexField(max_length=64)

    version = models.BigIntegerField(help_text='only version 1 valid in Bitcoin Core')
    locktime = models.BigIntegerField()

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.PROTECT,
        null=True,
    )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.txid = self._txid()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.txid

    def _txid(self):
        return hash256(self.serialize()).hex()

    def serialize(self):
        raw_tx = b''
        raw_tx += self.version.to_bytes(4, 'little')
        raw_tx += encode_as_varint(len(self.vin.all()))
        for input_ in self.vin.all():
            raw_tx += input_.serialize()
        raw_tx += encode_as_varint(len(self.vout.all()))
        for output in self.vout.all():
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
    vout = models.BigIntegerField()

    sequence = models.BigIntegerField()

    script_sig = HexField(max_length=20000)

    def serialize(self):
        raw_tx = b''
        raw_tx += bytes.fromhex(self.txid)
        raw_tx += self.vout.to_bytes(4, 'little')
        script_sig_as_bytes = bytes.fromhex(self.script_sig)
        raw_tx += encode_as_varint(len(script_sig_as_bytes))
        raw_tx += script_sig_as_bytes
        return raw_tx


class TransactionOutput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vout',
        on_delete=models.CASCADE,
    )

    value = BigIntegerField()
    n = models.BigIntegerField()

    script_pubkey = HexField(max_length=20000)

    class Meta:
        ordering = ['n', ]

    def serialize(self):
        raw_tx = b''
        raw_tx += self.value.to_bytes(8, 'little')
        script_pubkey_as_bytes = bytes.fromhex(self.script_pubkey)
        raw_tx += encode_as_varint(len(script_pubkey_as_bytes))
        raw_tx += script_pubkey_as_bytes
        return raw_tx
