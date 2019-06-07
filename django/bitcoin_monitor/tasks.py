import logging

from blocks.utils import parse_block

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, raw_block, height):
    """
    :param block_data: dictionary
        nested dictionary parsed from JSON,
        most elements are key-value string pairs,
        but some map a key to a list of
        transaction dictionaries
    """
    raw_block = bytes.fromhex(raw_block)
    block = parse_block(raw_block, height)
    # hash = block.hash()
    # verb = 'Created' if created else 'Skipping'
    # logger.debug('%s block %s', verb, hash)

#
# @celery_app.task(bind=True, ignore_result=True, max_retries=1)
# def process_transaction(self, raw_tx, block):
#     """
#     :param raw_tx:
#     """
#     transaction = parse_transaction(raw_tx)
#     transaction.block = block
#     transaction.save()
