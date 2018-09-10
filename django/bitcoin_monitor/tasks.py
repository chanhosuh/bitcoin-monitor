import logging

from blocks.models import Block
from transactions.models import Transaction, TransactionInput, TransactionOutput

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

    block = Block.objects.create(
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
def process_transaction(self, transaction_data):
    """
    :param transaction_data:
    """
    txid_ = transaction_data['txid']
    size = transaction_data['size']
    version = transaction_data['version']
    locktime = transaction_data['locktime']
    # hex_ = transaction_data['hex']

    block_hash = transaction_data['blockhash']
    block = Block.objects.get(hash=block_hash)

    transaction = Transaction.objects.create(
        txid=txid_,
        size=size,
        version=version,
        locktime=locktime,
        # hex=hex_,
        block=block,
    )
    logger.debug('Created transaction %s', txid_)

    for t_input in transaction_data['vin']:
        txid = t_input['txid']
        vout = t_input['vout']
        TransactionInput.objects.create(
            transaction=transaction,
            txid=txid,
            vout=vout,
        )
        logger.debug('Created input for %s', txid_)

    for t_output in transaction_data['vout']:
        value = t_output['value']
        n = t_output['n']
        TransactionOutput.objects.create(
            value=value,
            n=n,
        )
        logger.debug('Created output for %s', txid_)
