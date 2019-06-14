import logging
import time

from django.core.management.base import BaseCommand
from django.utils import autoreload

from bitcoin_monitor.tasks import process_block
from blocks.models import Block
from jsonrpc.client import RpcClient


logger = logging.getLogger(__name__)


def _process_blockchain():
    rpc_client = RpcClient()
    chain_length = rpc_client.get_block_count()
    logger.info('Blockchain length: %s', chain_length)

    # blocks are reverse ordered by height
    last_block = Block.objects.first()
    height = last_block.height if last_block else 0
    while True:
        logger.info('height: %s', height)
        block_hash = _retry_get_block_hash(rpc_client, height)
        logger.debug('Block hash: %s', block_hash)

        raw_block = rpc_client.get_block(block_hash, verbosity=0)
        process_block.si(raw_block, height).delay()

        height += 1


def _retry_get_block_hash(rpc_client, height):
    start = time.time()
    while True:
        try:
            block_hash = rpc_client.get_block_hash(height)
        except Exception:
            if time.time() - start > 300 * 60:
                raise Exception(
                    f'No block available for over 300 minutes at height {height}'
                )
            time.sleep(10)
        else:
            return block_hash


class Command(BaseCommand):
    """
    management command to run process using Django's autoreload
    functionality, so that it will restart upon any code change
    """
    def handle(self, *args, **options):
        logger.info('Autoreloading process_blockchain...')
        autoreload.main(_process_blockchain)
