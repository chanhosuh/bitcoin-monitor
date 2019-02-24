import json
import os

from django.test.testcases import TestCase

from bitcoin_monitor.settings import BASE_DIR
from bitcoin_monitor.tasks import process_block, process_transaction


class ProcessBlockchainTest(TestCase):

    def setUp(self):
        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'block.json')
        with open(filepath, 'r') as f:
            self.block = json.load(f)

        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'transactions.json')
        with open(filepath, 'r') as f:
            self.transactions = json.load(f)

    def test_process_block(self):
        process_block.si(self.block).apply()

    def test_process_transaction(self):
        block_hash = self.block['hash']
        process_block.si(self.block).apply()
        for transaction in self.transactions:
            process_transaction.si(transaction, block_hash).apply()
