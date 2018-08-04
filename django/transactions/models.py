from django.db import models
from model_utils.models import TimeStampedModel


class Transaction(TimeStampedModel):

    txid = ...
    size = ...
    version = ...
    locktime = ...

    block = models.ForeignKey(
        'blocks.Block',
        related_name='transactions',
        on_delete=models.CASCADE,
        null=True,
    )


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
