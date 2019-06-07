import logging

from blocks.utils import parse_block

from . import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True, ignore_result=True, max_retries=1)
def process_block(self, raw_block, height):  # pylint: disable=unused-argument
    """
    :param raw_block: string
        hex string for serialized block
    :param height: integer
        height on block chain (genesis block is 0)
    """
    raw_block = bytes.fromhex(raw_block)
    parse_block(raw_block, height)
