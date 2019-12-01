import json
import os

from django.test import TestCase

from bitcoin_monitor.settings import BASE_DIR
from blocks.utils import parse_block


DATA_DIR = os.path.join(BASE_DIR, "tests", "data")


class BlockUtilsTest(TestCase):
    def test_parse_block(self):
        block_data_filepath = os.path.join(DATA_DIR, "block_606079")
        with open(block_data_filepath, "r") as f:
            block_bytes = f.read()
            parse_block(block_bytes, 606079)
