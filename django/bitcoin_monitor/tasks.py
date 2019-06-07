import logging

from blocks.utils import parse_block

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, raw_block, height):  # pylint: disable=unused-argument
    """
    :param block_data: dictionary
        nested dictionary parsed from JSON,
        most elements are key-value string pairs,
        but some map a key to a list of
        transaction dictionaries
    """
    raw_block = bytes.fromhex(raw_block)
    parse_block(raw_block, height)
