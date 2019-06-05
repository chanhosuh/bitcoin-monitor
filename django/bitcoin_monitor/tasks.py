import logging

from blocks.models import Block
from transactions.models import parse_transaction

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, block_data):
    """
    :param block_data: dictionary
        nested dictionary parsed from JSON,
        most elements are key-value string pairs,
        but some map a key to a list of
        transaction dictionaries
    """
    hash_ = block_data['hash']
    confirmations = block_data['confirmations']
    size = block_data['size']
    stripped_size = block_data['strippedsize']
    weight = block_data['weight']
    height = block_data['height']
    version = block_data['version']
    merkle_root = block_data['merkleroot']
    time = block_data['time']
    median_time = block_data['mediantime']
    nonce = block_data['nonce']
    bits = block_data['bits']
    difficulty = block_data['difficulty']
    number_of_transactions = block_data['nTx']
    previous_block_hash = block_data['previousblockhash']
    next_block_hash = block_data['nextblockhash']

    block, created = Block.objects.get_or_create(
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
    verb = 'Created' if created else 'Skipping'
    logger.debug('%s block %s', verb, hash)
    return block


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_transaction(self, raw_tx, block):
    """
    :param raw_tx:
    """
    transaction = parse_transaction(raw_tx)
    transaction.block = block
    transaction.save()
