import logging

from django import db

from blocks.models import Block
from core.serialization import decode_varint, streamify_if_bytes
from transactions.models import Transaction, TransactionInput, TransactionOutput
from transactions.utilities import parse_transaction


logger = logging.getLogger(__name__)


@db.transaction.atomic
def parse_block(raw_block, height):
    """
    :param raw_block: string
        hex string for serialized block
    :param height: integer
        height on block chain (genesis block is 0)
    """
    block_bytes = bytes.fromhex(raw_block)
    byte_stream = streamify_if_bytes(block_bytes)

    version = int.from_bytes(byte_stream.read(4), "little")
    prev_hash = byte_stream.read(32).hex()[::-1]
    merkle_root = byte_stream.read(32).hex()[::-1]
    timestamp = int.from_bytes(byte_stream.read(4), "little")
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
    created_or_skipped = "created" if created else "skipped"

    if created:
        logger.debug(f"No block in DB for height {height}, creating...")

        tx_parts = [parse_transaction(byte_stream) for _ in range(num_transactions)]
        transactions = [t[0] for t in tx_parts]

        for transaction in transactions:
            transaction.block = block

        Transaction.objects.bulk_create(transactions)

        for transaction, inputs, outputs in tx_parts:
            for in_or_out in inputs + outputs:
                in_or_out.transaction = transaction
            TransactionInput.objects.bulk_create(inputs)
            TransactionOutput.objects.bulk_create(outputs)

        for transaction in transactions:
            # create txid (transaction hash) after the
            # related names, vin and vout, are attached
            transaction.txid = transaction._txid()

        Transaction.objects.bulk_update(transactions, ["txid"])

        logger.debug("Done creating transactions.")

    logger.info(f"block {created_or_skipped} at height {height}")

    return block
