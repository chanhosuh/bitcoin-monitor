import logging

from core.serialization import decode_varint, streamify_if_bytes
from transactions.models import (
    Transaction,
    TransactionInput,
    TransactionOutput,
    Witness,
)


logger = logging.getLogger(__name__)


def parse_transaction(byte_stream):
    byte_stream = streamify_if_bytes(byte_stream)

    version_bytes = byte_stream.read(4)
    version = int.from_bytes(version_bytes, "little")

    num_inputs = decode_varint(byte_stream)
    # a 0x00 here is the Segwit marker
    is_segwit = num_inputs == 0
    if is_segwit:
        # next byte is flag
        _ = byte_stream.read(1)[0]  # should be nonzero (0x01 currently)
        num_inputs = decode_varint(byte_stream)

    inputs = [parse_input(byte_stream) for _ in range(num_inputs)]

    num_outputs = decode_varint(byte_stream)
    outputs = [parse_output(byte_stream, n) for n in range(num_outputs)]

    if is_segwit:
        witnesses = [parse_witness(byte_stream) for _ in range(num_inputs)]
    else:
        witnesses = []

    locktime_bytes = byte_stream.read(4)
    locktime = int.from_bytes(locktime_bytes, "little")

    transaction = Transaction(version=version, locktime=locktime)

    return transaction, inputs, outputs, witnesses


def parse_input(byte_stream):
    prev_txid = byte_stream.read(32).hex()[::-1]
    prev_index = int.from_bytes(byte_stream.read(4), "little")

    len_script_sig = decode_varint(byte_stream)
    script_sig = byte_stream.read(len_script_sig).hex()

    sequence = int.from_bytes(byte_stream.read(4), "little")

    tx_input = TransactionInput(
        txid=prev_txid, vout=prev_index, script_sig=script_sig, sequence=sequence,
    )
    return tx_input


def parse_output(byte_stream, n):
    value = int.from_bytes(byte_stream.read(8), "little")
    len_script_pubkey = decode_varint(byte_stream)
    script_pubkey = byte_stream.read(len_script_pubkey).hex()

    tx_output = TransactionOutput(value=value, script_pubkey=script_pubkey, n=n)
    return tx_output


def parse_witness(byte_stream):
    num_stack_items = decode_varint(byte_stream)

    stack_items = []
    for _ in range(num_stack_items):
        size = decode_varint(byte_stream)
        item = byte_stream.read(size)
        stack_items.append(item)

    witness = Witness(stack_items=stack_items)
    return witness
