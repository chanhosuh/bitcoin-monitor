import json
import os

from django.forms.models import model_to_dict
from django.test.testcases import TestCase

from bitcoin_monitor.settings import BASE_DIR
from bitcoin_monitor.tasks import process_block, process_transaction
from blocks.models import Block


class ProcessBlockchainTest(TestCase):

    def setUp(self):
        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'block.json')
        with open(filepath, 'r') as f:
            self.block = json.load(f)

        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'transactions.json')
        with open(filepath, 'r') as f:
            self.transactions = json.load(f)

        self.block_hash = self.block['hash']

    def test_process_block(self):
        process_block.si(self.block).apply()
        try:
            block = Block.objects.get(hash=self.block_hash)
        except Block.DoesNotExist:
            self.fail(f'Block was not created with hash: {self.block_hash}')

        block_dict = model_to_dict(block, exclude=['id', ])
        self.assertDictEqual(self.block, block_dict)

    def test_process_transaction(self):
        process_block.si(self.block).apply()
        for transaction in self.transactions:
            process_transaction.si(transaction, self.block_hash).apply()
