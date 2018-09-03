from django.db import models
from model_utils.models import TimeStampedModel

# from bitcoind RPC output
[
    'hash', 'confirmations', 'strippedsize', 'size', 'weight', 'height', 'version',
    'versionHex', 'merkleroot', 'tx', 'time', 'mediantime', 'nonce', 'bits', 'difficulty',
    'chainwork', 'nTx', 'previousblockhash',
]


class Block(TimeStampedModel):

    header = models.OneToOneField('blocks.BlockHeader', on_delete=models.CASCADE)
    hash = ...
    confirmations = ...
    stripped_size = ...
    size = ...
    weight = ...
    height = ...
    version = ...
    version_hex = ...
    merkle_root = ...
    tx = ...
    time = ...
    median_time = ...
    nonce = ...
    bits = ...
    difficulty = ...
    chain_work = ...
    nTx = ...
    previous_block_hash = ...


class BlockHeader(TimeStampedModel):

    version = models.IntegerField()
    hash_prev_block = models.CharField()
    hash_merkle_root = models.CharField()
    time = ...
    bits = ...
    nonce = ...