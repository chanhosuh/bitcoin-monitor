"""
http://chainquery.com/bitcoin-api/getblock

getblock "blockhash" ( verbosity )

If verbosity is 0, returns a string that is serialized, hex-encoded data for block 'hash'.
If verbosity is 1, returns an Object with information about block <hash>.
If verbosity is 2, returns an Object with information about block <hash> and information about each transaction.

Arguments:
1. "blockhash"          (string, required) The block hash
2. verbosity              (numeric, optional, default=1)
                          0 for hex encoded data
                          1 for a json object
                          2 for json object with transaction data

Result (for verbosity = 0):
"data"             (string) A string that is serialized, hex-encoded data for block 'hash'.

Result (for verbosity = 1):
{
  "hash" : "hash",     (string) the block hash (same as provided)
  "confirmations" : n,   (numeric) The number of confirmations, or -1 if the block is not on the main chain
  "size" : n,            (numeric) The block size
  "strippedsize" : n,    (numeric) The block size excluding witness data
  "weight" : n           (numeric) The block weight as defined in BIP 141
  "height" : n,          (numeric) The block height or index
  "version" : n,         (numeric) The block version
  "versionHex" : "00000000", (string) The block version formatted in hexadecimal
  "merkleroot" : "xxxx", (string) The merkle root
  "tx" : [               (array of string) The transaction ids
     "transactionid"     (string) The transaction id
     ,...
  ],
  "time" : ttt,          (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
  "mediantime" : ttt,    (numeric) The median block time in seconds since epoch (Jan 1 1970 GMT)
  "nonce" : n,           (numeric) The nonce
  "bits" : "1d00ffff", (string) The bits
  "difficulty" : x.xxx,  (numeric) The difficulty
  "chainwork" : "xxxx",  (string) Expected number of hashes required to produce the chain up to this block (in hex)
  "previousblockhash" : "hash",  (string) The hash of the previous block
  "nextblockhash" : "hash"       (string) The hash of the next block
}

Result (for verbosity = 2):
{
  ...,                     Same output as verbosity = 1.
  "tx" : [               (array of Objects)
         ...,            The transactions in the format of the getrawtransaction RPC.
                         Different from verbosity = 1 "tx" result.
  ],
  ,...                     Same output as verbosity = 1.
}

"""
from django.db import models

from model_utils.models import TimeStampedModel

from core.model_fields import HexField


class Block(TimeStampedModel):

    # header = models.OneToOneField('blocks.BlockHeader', on_delete=models.CASCADE)
    hash = HexField(max_length=64, unique=True, help_text='block hash in hex (32 bytes)')
    # integer, -1 means not on the best blockchain
    confirmations = models.IntegerField()

    # size of block in bytes
    size = models.IntegerField()
    # size of block, excluding witness data, in bytes
    stripped_size = models.IntegerField()
    # block weight (see BIP 141)
    weight = models.IntegerField()
    # block height (zero-indexed)
    height = models.PositiveIntegerField()
    # block version
    version = models.PositiveIntegerField()
    # block version in hex
#     version_hex = models.CharField()
    # 32 byte hash in hex
    merkle_root = HexField(max_length=64)
    # verbosity 1: array of transaction ids
    # verbosity 2: array of JSON, getrawtransaction format
    # tx = ...  # use foreign key from transaction to block
    # block time in seconds since unix epoch
    time = models.PositiveIntegerField()
    # median block time in seconds since unix epoch
    median_time = models.PositiveIntegerField()
    # puzzle nonce: int
    nonce = models.BigIntegerField()
    # string
    bits = HexField(max_length=8)
    # float
    difficulty = models.DecimalField(decimal_places=10, max_digits=25)
    # expected number of hashes to produce blockchain up to this block, in hex
    # chain_work = models.CharField()
    # len of tx: int
    number_of_transactions = models.PositiveIntegerField()
    previous_block_hash = HexField(max_length=64)
    next_block_hash = HexField(max_length=64, null=True)

#
# class BlockHeader(TimeStampedModel):
#
#     version = models.IntegerField()
#     hash_prev_block = models.CharField()
#     hash_merkle_root = models.CharField()
#     time = ...
#     bits = ...
#     nonce = ...
