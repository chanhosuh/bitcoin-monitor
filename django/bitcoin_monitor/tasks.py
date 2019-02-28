import logging

from blocks.models import Block
from core.bitcoin import Bitcoin
from transactions.models import UTXO, CoinbaseTransaction, Transaction, TransactionOutput

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

    _, created = Block.objects.get_or_create(
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
    logger.debug('%s block %s', verb, hash_)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_transaction(self, transaction_data, block_hash):
    """
    :param transaction_data:
    """
    txid_ = transaction_data['txid']
    size = transaction_data['size']
    version = transaction_data['version']
    locktime = transaction_data['locktime']
    # hex_ = transaction_data['hex']

    # For some reason, block hash is missing, even with verbosity=2,
    # which according to bitcoin core docs, should have it;
    # instead, we pass it in, since all transactions we process
    # are coming from a block anyway.
    # --------------------------------------
    # block_hash = transaction_data['blockhash']
    block = Block.objects.get(hash=block_hash)

    transaction, created = Transaction.objects.get_or_create(
        txid=txid_,
        size=size,
        version=version,
        locktime=locktime,
        # hex=hex_,
        block=block,
    )
    verb = 'Created' if created else 'Skipping'
    logger.debug('%s transaction %s', verb, txid_)

    for t_input in transaction_data['vin']:
        if 'coinbase' in t_input:
            CoinbaseTransaction.objects.get_or_create(
                coinbase=t_input['coinbase'],
                sequence=t_input['sequence'],
            )
            logger.debug('Created coinbase input')
        else:
            txid = t_input['txid']
            vout = t_input['vout']
            _, created = UTXO.objects.get_or_create(
                transaction=transaction,
                txid=txid,
                vout=vout,
            )
            verb = 'Created' if created else 'Skipping'
            logger.debug('%s input for %s', verb, txid_)

    for t_output in transaction_data['vout']:
        value = Bitcoin(t_output['value'])
        n = t_output['n']
        _, created = TransactionOutput.objects.get_or_create(
            transaction=transaction,
            value=value,
            n=n,
        )
        verb = 'Created' if created else 'Skipping'
        logger.debug('%s output for %s', verb, txid_)
