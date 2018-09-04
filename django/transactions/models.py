from django.db import models

from model_utils.models import TimeStampedModel

from core.model_fields import HashField


class Transaction(TimeStampedModel):

    txid = HashField()
    size = models.PositiveIntegerField()
    version = models.PositiveIntegerField()
    locktime = models.PositiveIntegerField()
    hex = models.CharField()  # serialized, hex-encoded transaction data

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.CASCADE,
        null=True,
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


class TransactionInput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vin',
        on_delete=models.CASCADE,
    )

    # identify unspent transaction output
    txid = HashField()
    vout = models.PositiveIntegerField()

    # script_sig = models.CharField()
    sequence = models.PositiveIntegerField()


class TransactionOutput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vout',
        on_delete=models.CASCADE,
    )

    value = models.IntegerField()
    n = models.PositiveIntegerField()
    # script_pub_key = models.CharField()
