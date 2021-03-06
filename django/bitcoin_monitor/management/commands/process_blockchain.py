import logging
import time

from django.core.management.base import BaseCommand
from django.utils import autoreload

import redis

from bitcoin_monitor import settings
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

        if height % 100 == 0:
            _wait_if_task_queue_full()

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


def _wait_if_task_queue_full(size=100):
    r = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
    while r.llen('celery') > size:
        logger.info('Waiting...')
        time.sleep(20)


_throttling = False


def _is_throttling(height, threshold):
    global _throttling
    last_block = Block.objects.first()
    num_blocks_ahead = height - last_block.height

    if num_blocks_ahead > threshold:
        if not _throttling:
            logger.info(
                'Throttling: creating tasks too quickly compared to blocks processed.'
            )
            _throttling = True
    else:
        _throttling = False

    return _throttling


class Command(BaseCommand):
    """
    management command to run process using Django's autoreload
    functionality, so that it will restart upon any code change
    """
    def handle(self, *args, **options):
        logger.info('Autoreloading process_blockchain...')
        autoreload.run_with_reloader(_process_blockchain)
