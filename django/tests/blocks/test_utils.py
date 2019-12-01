import os

from django.test import TestCase

from bitcoin_monitor.settings import BASE_DIR
from blocks.utils import parse_block


DATA_DIR = os.path.join(BASE_DIR, "tests", "data")


class BlockUtilsTest(TestCase):
    def test_parse_block(self):
        height = 606079
        block_hex_filepath = os.path.join(DATA_DIR, f"block_{height}")
        with open(block_hex_filepath, "r") as f:
            block_hex = f.read()
            block = parse_block(block_hex, height)

        self.assertEqual(block.num_transactions, 2458)
        self.assertEqual(block.height, height)

        self.assertEqual(
            block.hash,
            "0000000000000000000d459e6ac961faac4eb72e4d4eaedf0bf6997dfb1b42eb",
        )
