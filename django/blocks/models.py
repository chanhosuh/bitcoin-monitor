from django.db import models
from model_utils.models import TimeStampedModel


if False:
    import bitcoin.rpc
    proxy = bitcoin.rpc.Proxy(service_url='http://user:password@bitcoind:8332')
    block = proxy.getblock(proxy.getblockhash(0))
    """
    In [4]: block
    Out[4]: CBlock(1, lx(0000000000000000000000000000000000000000000000000000000000000000), lx(4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b), 1231006505, 0x1d00ffff, 0x7c2bac1d)
    """


class Block(TimeStampedModel):

    header = models.OneToOneField('blocks.BlockHeader', on_delete=models.CASCADE)


class BlockHeader(TimeStampedModel):

    version = models.IntegerField()
    hash_prev_block = models.CharField()
    hash_merkle_root = models.CharField()
    time = ...
    bits = ...
    nonce = ...
