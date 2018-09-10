import logging

from blocks.models import Block

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, block):
    """
    :param block: dictionary
        nested dictionary parsed from JSON,
        most elements are key-value string pairs,
        but some map a key to a list of
        transaction dictionaries
    """
    hash_ = block['hash']
    confirmations = block['confirmations']
    size = block['size']
    stripped_size = block['strippedsize']
    weight = block['weight']
    height = block['height']
    version = block['version']
    merkle_root = block['merkleroot']
    time = block['time']
    median_time = block['mediantime']
    nonce = block['nonce']
    bits = block['bits']
    difficulty = block['difficulty']
    number_of_transactions = block['nTx']
    previous_block_hash = block['previousblockhash']
    next_block_hash = block['nextblockhash']

    Block.objects.create(
        hash=hash_,
        confirmations=confirmations,
        size=size,
        stripped_size=stripped_size,
        weight=weight,
        height=height,
        version=version,
        merkle_root=merkle_root,
        time=time,
        median_time=median_time,
        nonce=nonce,
        bits=bits,
        difficulty=difficulty,
        number_of_transactions=number_of_transactions,
        previous_block_hash=previous_block_hash,
        next_block_hash=next_block_hash,
    )
    logger.debug('Created block %s', hash)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_transaction(self, transaction):
    """

    :param transaction:
    """
