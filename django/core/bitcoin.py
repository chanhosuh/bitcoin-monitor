from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from functools import total_ordering

from django.utils.deconstruct import deconstructible


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
    Conceptually, a Bitcoin object disallows some arithmetic operations (such as
    multiplying Bitcoin by Bitcoin) while allowing others (adding Bitcoin to Bitcoin or
    taking a fraction of Bitcoin).

    Since there is a minimum unit of bitcoin, a satoshi, it makes sense to do
    arithmetic operations on satoshis (integers) as much as possible, while using
    appropriately quantized Decimals when needed.  This class wraps around both
    integer and Decimal amounts appropriately.
    """

    DECIMAL_PLACES = 8  # minimal unit is 1e-8, a "satoshi"

    def __init__(self, value):
        """ value (int): amount in satoshis """
        try:
            value = self.quantize(value)
            self.satoshis = int(value)
            self.decimal = value / 10 ** self.DECIMAL_PLACES
        except (ValueError, TypeError, InvalidOperation):
            raise BitcoinValueError(
                "Canot create Bitcoin with value '{}' of type {}".format(
                    value, type(value).__name__,
                )
            )

    def to_bytes(self, *args, **kwargs):
        """
        Convenience method, since serialization is everywhere in Bitcoin!
        Since the usual format sent over the wire is satoshis encoded
        as bytes, we delegate to the 'satoshis' attribute.
        """
        return self.satoshis.to_bytes(*args, **kwargs)

    def _is_bitcoin(self, operand):
        return isinstance(operand, Bitcoin)

    def __eq__(self, other):
        if self._is_bitcoin(other):
            return self.satoshis == other.satoshis
        return False

    def __lt__(self, other):
        if self._is_bitcoin(other):
            return self.satoshis < other.satoshis
        return NotImplemented

    def __hash__(self):
        return hash(self.satoshis)

    def __pos__(self):
        return self

    def __neg__(self):
        return Bitcoin(-1 * self.satoshis)

    def __add__(self, other):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError("Cannot add Bitcoin object to non-Bitcoin object.")
        return Bitcoin(self.satoshis + other.satoshis)

    def __sub__(self, other):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError(
                "Cannot subtract non-Bitcoin object from Bitcoin object."
            )
        return Bitcoin(self.satoshis - other.satoshis)

    def __rsub__(self, other):
        if not self._is_bitcoin(other):
            raise BitcoinTypeError(
                "Cannot subtract Bitcoin object from non-Bitcoin object."
            )
        return Bitcoin(other.satoshis - self.satoshis)

    def __mul__(self, other):
        if self._is_bitcoin(other):
            raise BitcoinTypeError(
                "Cannot multiply Bitcoin object by another Bitcoin object."
            )
        return Bitcoin(self.satoshis * other)

    def __truediv__(self, other):
        if isinstance(other, Bitcoin):
            return self.decimal / other.decimal
        return Bitcoin(self.satoshis / other)

    def __rtruediv__(self, other):  # pylint: disable=unused-argument
        raise BitcoinTypeError("Cannot divide non-Bitcoin object by Bitcoin object.")

    __radd__ = __add__
    __rmul__ = __mul__

    def __repr__(self):
        return "Bitcoin('{!s}')".format(self.decimal)

    def __str__(self):
        return str(self.decimal)

    @classmethod
    def quantize(cls, dec):
        return dec.quantize(
            Decimal("10") * (-1 * cls.DECIMAL_PLACES), rounding=ROUND_HALF_EVEN
        )
