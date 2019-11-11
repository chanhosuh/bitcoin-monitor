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
import datetime

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models

from model_utils.models import TimeStampedModel

from core.hash_utils import hash256
from core.model_fields import HexField


class Block(TimeStampedModel):

    hash = HexField(primary_key=True, max_length=64)

    # block height (zero-indexed)
    height = models.PositiveIntegerField(help_text='zero-index block height')

    prev_hash = HexField(max_length=64, help_text='block hash in hex (32 bytes)')

    # block version
    version = models.PositiveIntegerField()

    # 32 byte hash in hex
    merkle_root = HexField(max_length=64)

    # block time in seconds since unix epoch
    timestamp = models.PositiveIntegerField()

    # target in "bits" format
    bits = HexField(max_length=8)

    # used for proof-of-work
    nonce = HexField(max_length=8)

    num_transactions = models.PositiveIntegerField()

    class Meta:
        ordering = ('-height', )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.hash = self._hash()
        super().save(*args, **kwargs)

    def __repr__(self):
        return f'<Block height={self.height}, hash={self.hash}>'

    def __str__(self):
        return self.hash

    def _hash(self):
        return hash256(self.raw_header).hex()[::-1]

    @property
    def raw_header(self):
        raw_header = b''
        raw_header += self.version.to_bytes(4, 'little')
        raw_header += bytes.fromhex(self.prev_hash[::-1])
        raw_header += bytes.fromhex(self.merkle_root[::-1])
        raw_header += self.timestamp.to_bytes(4, 'little')
        raw_header += bytes.fromhex(self.bits)
        raw_header += bytes.fromhex(self.nonce)
        return raw_header

    @property
    def age(self):
        dt = datetime.datetime.utcfromtimestamp(self.timestamp)
        return naturaltime(dt)
