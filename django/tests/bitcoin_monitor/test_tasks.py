import json
import os

from django.test.testcases import TestCase

from bitcoin_monitor.settings import BASE_DIR


class ProcessBlockTest(TestCase):

    def setUp(self):
        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'block.json')
        with open(filepath, 'r') as f:
            self.block = json.load(f)

    def test_something(self):
        print(self.block)


class ProcessTransactionTest(TestCase):

    def setUp(self):
        filepath = os.path.join(BASE_DIR, 'tests', 'data', 'transactions.json')
        with open(filepath, 'r') as f:
            self.transactions = json.load(f)

    def test_something(self):
        print(self.transactions)
