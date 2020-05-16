import pickle
from builtins import AttributeError
from decimal import Decimal
from unittest import TestCase

from core.bitcoin import Bitcoin, BitcoinTypeError


# pylint: disable=expression-not-assigned
class BitcoinTest(TestCase):
    def test_make_bitcoin(self):
        """ test the different ways we can make Bitcoin """
        # pylint: disable=broad-except
        try:
            Bitcoin(1)
        except Exception:
            self.fail("Could not make Bitcoin from integer")

        try:
            Bitcoin("1")
        except Exception:
            self.fail("Could not make Bitcoin from string")

        try:
            Bitcoin("1.000000")
        except Exception:
            self.fail("Could not make Bitcoin from float as string")

        try:
            Bitcoin(1.000000001)
        except Exception:
            self.fail("Could not make Bitcoin from float")

        try:
            Bitcoin(Bitcoin(1))
        except Exception:
            self.fail("Could not make Bitcoin from Bitcoin")

    def test_add(self):
        bitcoin_1 = Bitcoin(1)
        bitcoin_2 = Bitcoin(2)

        expected_sum = Bitcoin(3)
        self.assertEqual(expected_sum, bitcoin_1 + bitcoin_2)

        with self.assertRaises(BitcoinTypeError):
            Bitcoin(1) + 2
        with self.assertRaises(BitcoinTypeError):
            1 + Bitcoin(2)

    def test_subtract(self):
        bitcoin_1 = Bitcoin("2")
        bitcoin_2 = Bitcoin("1")

        expected_difference = Bitcoin(1)
        self.assertEqual(expected_difference, bitcoin_1 - bitcoin_2)

        with self.assertRaises(BitcoinTypeError):
            Bitcoin(1) - Decimal(1)
        with self.assertRaises(BitcoinTypeError):
            Decimal(1) - Bitcoin(1)

    def test_multiply(self):

        with self.assertRaises(BitcoinTypeError):
            Bitcoin(1) * Bitcoin(2)

        result = Bitcoin(4) * Decimal("1.250000001")
        expected_result = Bitcoin(5)
        self.assertEqual(result, expected_result)

        result = Bitcoin(1) * Decimal("0.2575")
        expected_result = Bitcoin(0)
        self.assertEqual(result, expected_result)

        result = Bitcoin(4) * Decimal("0.2575")
        expected_result = Bitcoin(1)
        self.assertEqual(result, expected_result)

        result = Decimal(1) * Bitcoin(22)
        expected_result = Bitcoin(22)
        self.assertEqual(result, expected_result)

    def test_divide(self):
        with self.assertRaises(BitcoinTypeError):
            Decimal("10") / Bitcoin("2.000000001")

        result = Bitcoin("10") / Decimal("2.0")
        expected_result = Bitcoin(5)
        self.assertEqual(result, expected_result)

        result = Bitcoin(100) / Bitcoin(25)
        expected_result = Decimal("4.00000000")
        self.assertEqual(result, expected_result)

    def test_comparison(self):
        bitcoin_1 = Bitcoin(1.9)
        bitcoin_2 = Bitcoin(3)

        self.assertEqual(bitcoin_1, bitcoin_1, "bitcoin object should equal itself")
        self.assertEqual(
            bitcoin_1, Bitcoin(1.9), "same expressions should give equal bitcoin",
        )
        self.assertEqual(
            bitcoin_1, Bitcoin(2), "rounding to satoshis should give equal bitcoin"
        )
        self.assertNotEqual(bitcoin_1, bitcoin_2)
        self.assertLess(bitcoin_1, bitcoin_2)
        self.assertLessEqual(bitcoin_1, bitcoin_2)
        self.assertLessEqual(bitcoin_1, Bitcoin(1.5))
        self.assertGreater(bitcoin_2, bitcoin_1)
        self.assertGreaterEqual(bitcoin_2, Bitcoin(3.1))

    def test_error_on_comparing_to_another_type(self):
        bitcoin = Bitcoin(1)
        dec = Decimal(2)

        with self.assertRaises(TypeError):
            bitcoin < dec  # noqa

    def test_different_types_not_equal(self):
        """ since Python standard behavior is to allow equality
        checks between differently-typed objects (but to return
        False in those cases), we should test for that """
        bitcoin = Bitcoin(1)

        self.assertNotEqual(bitcoin, 1.0)
        self.assertNotEqual(bitcoin, Decimal(1))

        # yep, Python even lets you check if a float is
        # equal to a module
        # In [1]: import os; import math
        # In [2]: os == math.pi
        # Out[2]: False
        import os

        self.assertNotEqual(bitcoin, os)

    def test_immutability(self):
        """ test Bitcoin instance is immutable """
        bitcoin = Bitcoin("1")

        with self.assertRaises(
            AttributeError, msg='should not be able to modify "satoshis" attribute',
        ):
            bitcoin.satoshis = 123

        with self.assertRaises(
            AttributeError, msg='should not be able to modify "decimal" attribute',
        ):
            bitcoin.decimal = Decimal("2")

        with self.assertRaises(
            AttributeError, msg="should not be able to add attribute to Bitcoin",
        ):
            bitcoin.foo = "foo"  # pylint: disable=assigning-non-slot

        new_bitcoin = Bitcoin(bitcoin)
        self.assertIs(
            new_bitcoin, bitcoin, "making bitcoin from bitcoin should not copy"
        )

    def test_pickle(self):
        """ test we can pickle Bitcoin """
        bitcoin = Bitcoin("1")

        pickled_bitcoin = pickle.dumps(bitcoin)
        unpickled_bitcoin = pickle.loads(pickled_bitcoin)

        self.assertEqual(unpickled_bitcoin, bitcoin)

    def test_intern_pool(self):
        """ test Bitcoin instances are re-used """
        bitcoin_1 = Bitcoin("1")
        bitcoin_2 = Bitcoin("1")

        self.assertIs(bitcoin_1, bitcoin_2)
