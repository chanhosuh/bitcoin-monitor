from django.db import models
from model_utils.models import TimeStampedModel


class Transaction(TimeStampedModel):

    txid = ...
    size = ...
    version = ...
    locktime = ...
    hex = ...

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.CASCADE,
        null=True,
    )

    @property
    def hash(self):
        """ seems to be the same as txid """
        return self.txid

    @property
    def vsize(self):
        """ seems to be the same as size """
        return self.size


# from bitcoind RPC output
['txid', 'hash', 'version', 'size', 'vsize', 'locktime', 'vin', 'vout', 'hex']


class TransactionInput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vin',
        on_delete=models.CASCADE,
    )

    txid = ...
    vout = ...
    script_sig = ...
    sequence = ...


class TransactionOutput(TimeStampedModel):

    transaction = models.ForeignKey(
        'transactions.Transaction',
        related_name='vout',
        on_delete=models.CASCADE,
    )

    value = models.IntegerField(null=False)
    n = ...
    script_pub_key = ...
