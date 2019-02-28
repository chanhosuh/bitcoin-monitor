"""
http://chainquery.com/bitcoin-api/getrawtransaction
"""
from django.db import models

from model_utils.models import TimeStampedModel
from polymorphic.models import PolymorphicModel

from core.model_fields import BitcoinField, HexField


class TransactionInput(PolymorphicModel, TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vin',
        on_delete=models.CASCADE,
    )


class CoinbaseTransaction(TransactionInput):

    coinbase = HexField(max_length=200)
    sequence = models.BigIntegerField()


class Transaction(TimeStampedModel):

    txid = HexField(max_length=64, unique=True, help_text='transaction hash in hex (32 bytes)')
    size = models.PositiveIntegerField()
    version = models.PositiveIntegerField()
    locktime = models.PositiveIntegerField()
    # hex = HexField(max_length=256)  # serialized, hex-encoded transaction data

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.CASCADE,
    )

# differs for witness transactions
#     @property
#     def hash(self):
#         """ seems to be the same as txid """
#         return self.txid
#
#     @property
#     def vsize(self):
#         """ seems to be the same as size """
#         return self.size


# from bitcoind RPC output
['txid', 'hash', 'version', 'size', 'vsize', 'locktime', 'vin', 'vout', 'hex']


class UTXO(TransactionInput):

    # identify unspent transaction output
    txid = HexField(max_length=64, help_text='transaction hash in hex (32 bytes)')
    vout = models.PositiveIntegerField()

    class Meta:
        unique_together = (('txid', 'vout'), )

    # "scriptSig": {     (json object) The script
    #   "asm": "asm",  (string) asm
    #   "hex": "hex"   (string) hex
    # },
    # "sequence": n      (numeric) The script sequence number
    # script_sig = models.CharField()
    # sequence = models.PositiveIntegerField()


class TransactionOutput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vout',
        on_delete=models.CASCADE,
    )

    value = BitcoinField()
    n = models.PositiveIntegerField()

    # "scriptPubKey" : {          (json object)
    #   "asm" : "asm",          (string) the asm
    #   "hex" : "hex",          (string) the hex
    #   "reqSigs" : n,            (numeric) The required sigs
    #   "type" : "pubkeyhash",  (string) The type, eg 'pubkeyhash'
    #   "addresses" : [           (json array of string)
    #     "address"        (string) bitcoin address
    #     ,...
    #   ]
    # }
    # script_pub_key = models.CharField()
