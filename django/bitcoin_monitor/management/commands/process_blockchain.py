import logging

from django.core.management.base import BaseCommand
from django.utils import autoreload

from bitcoin_monitor.tasks import process_block, process_transaction
from jsonrpc.client import RpcClient


logger = logging.getLogger(__name__)


def read_blocks():
    rpc_client = RpcClient()
    chain_length = rpc_client.get_block_count()
    logger.info('Blockchain length: %s', chain_length)

    # for now we have to traverse the blockchain backwards,
    # as we are pruning it to save storage
    # for height in range(1, chain_length):
    for height in range(chain_length - 1, 0, -1):
        logger.debug('height: %s', height)
        block_hash = rpc_client.get_block_hash(height)
        logger.debug('Block hash: %s', block_hash)
        block = rpc_client.get_block(block_hash)
        process_block.si(block).delay()
        # transactions = rpc_client.get_transactions(block_hash)
        # for transaction in transactions:
        #     process_transaction.si(transaction).delay()


class Command(BaseCommand):
    """ management command to run process using Django's autoreload functionality,
    so that it will restart upon any code change """

    def handle(self, *args, **options):
        logger.info('Autoreloading read_blocks ...')
        autoreload.main(read_blocks)
