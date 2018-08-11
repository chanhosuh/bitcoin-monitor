from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from functools import total_ordering
from typing import Union

from django.utils.deconstruct import deconstructible


def quantize_to(dec, places):
    return dec.quantize(Decimal(10) ** (-1 * places), rounding=ROUND_HALF_EVEN)


class BitcoinError(RuntimeError):
    pass


class BitcoinTypeError(TypeError, BitcoinError):
    pass


class BitcoinValueError(ValueError, BitcoinError):
    pass


@deconstructible
@total_ordering
class Bitcoin:
    """
    A wrapper class around Decimal, to ensure that allowed arithmetic operations
    result in a Decimal quantized to the correct number of decimal places,
    with appropriate rounding.

    Conceptually, a Bitcoin object disallows some arithmetic operations (such as
    multiplying Bitcoin by Bitcoin) while allowing others (adding Bitcoin to Bitcoin or
    taking a fraction of Bitcoin).
    """

    DECIMAL_PLACES = 8  # minimal unit is 1e-8, a "satoshi"

    def __init__(self, value: Union[Decimal, str, int]='0'):
        try:
            self.decimal = self.quantize_to_currency(Decimal(value))
        except (InvalidOperation, TypeError):
            raise BitcoinValueError(
                "Canot create Bitcoin with value '{}' of type {}".format(
                    value, type(value).__name__,
                )
            )

    def _is_bitcoin(self, operand):
        return isinstance(operand, Bitcoin)

    def __eq__(self, other: Union['Bitcoin', None]):
        if self._is_bitcoin(other):
            return self.decimal == other.decimal
        return False

    def __lt__(self, other: 'Bitcoin'):
        if self._is_bitcoin(other):
            return self.decimal < other.decimal
        return NotImplemented

    def __hash__(self):
        return hash(self.decimal)

    def __pos__(self):
        return self

    def __neg__(self):
        return Bitcoin(-1 * self.decimal)

    def __add__(self, other: 'Bitcoin'):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError('Cannot add Bitcoin object to non-Bitcoin object.')
        return Bitcoin(self.decimal + other.decimal)

    def __sub__(self, other: 'Bitcoin'):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError('Cannot subtract non-Bitcoin object from Bitcoin object.')
        return Bitcoin(self.decimal - other.decimal)

    def __rsub__(self, other: 'Bitcoin'):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError('Cannot subtract Bitcoin object from non-Bitcoin object.')
        return Bitcoin(other.decimal - self.decimal)

    def __mul__(self, other: Union[Decimal, int]):
        if self._is_bitcoin(other):
            raise BitcoinTypeError('Cannot multiply Bitcoin object by another Bitcoin object.')
        return Bitcoin(self.decimal * other)

    def __truediv__(self, other: Union[Decimal, int, 'Bitcoin']):
        if isinstance(other, Bitcoin):
            return self.decimal / other.decimal
        return Bitcoin(self.decimal / other)

    def __rtruediv__(self, other):  # pylint: disable=unused-argument
        raise BitcoinTypeError('Cannot divide non-Bitcoin object by Bitcoin object.')

    __radd__ = __add__
    __rmul__ = __mul__

    def __repr__(self):
        return "Bitcoin('{!s}')".format(self.decimal)

    def __str__(self):
        return str(self.decimal)

    @classmethod
    def quantize_to_currency(cls, dec):
        return quantize_to(dec, cls.DECIMAL_PLACES)

    # Decimal methods
    def as_tuple(self):
        return self.decimal.as_tuple()
