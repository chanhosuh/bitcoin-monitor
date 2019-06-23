import logging

from blocks.models import Block
from core.serialization import decode_varint, streamify_if_bytes
from transactions.models import Transaction
from transactions.utilities import parse_transaction


logger = logging.getLogger(__name__)


def parse_block(byte_stream, height):
    byte_stream = streamify_if_bytes(byte_stream)

    version = int.from_bytes(byte_stream.read(4), 'little')
    prev_hash = byte_stream.read(32).hex()[::-1]
    merkle_root = byte_stream.read(32).hex()[::-1]
    timestamp = int.from_bytes(byte_stream.read(4), 'little')
    bits = byte_stream.read(4).hex()
    nonce = byte_stream.read(4).hex()

    num_transactions = decode_varint(byte_stream)

    block, created = Block.objects.get_or_create(
        height=height,
        version=version,
        prev_hash=prev_hash,
        merkle_root=merkle_root,
        timestamp=timestamp,
        bits=bits,
        nonce=nonce,
        num_transactions=num_transactions,
    )
    created_or_skipped = 'created' if created else 'skipped'
    logger.debug(f'block {created_or_skipped} at height {height}')

    transactions = [parse_transaction(byte_stream) for _ in range(num_transactions)]

    for transaction in transactions:
        transaction.block = block

    Transaction.objects.bulk_create(transactions)

    logger.debug('Done creating transactions.')

    return block
