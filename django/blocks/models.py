from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Block(TimeStampedModel):

    header = models.OneToOneField('blocks.BlockHeader', on_delete=models.CASCADE)


class BlockHeader(TimeStampedModel):

    version = models.IntegerField()
    hash_prev_block = models.CharField()
    hash_merkle_root = models.CharField()
    time = ...
    bits = ...
    nonce = ...
