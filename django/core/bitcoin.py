import threading
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from functools import total_ordering
from weakref import WeakValueDictionary


class BitcoinError(RuntimeError):
    pass


class BitcoinTypeError(TypeError, BitcoinError):
    pass


class BitcoinValueError(ValueError, BitcoinError):
    pass


class BitcoinAttributeError(AttributeError, BitcoinError):
    pass


# pylint: disable=no-member
@total_ordering
class Bitcoin:
    """
    Conceptually, a Bitcoin object disallows some arithmetic operations
    (such as multiplying Bitcoin by Bitcoin) while allowing others
    (adding Bitcoin to Bitcoin or taking a fraction of Bitcoin).

    Since there is a minimum unit of bitcoin, a satoshi, it makes sense
    to do arithmetic operations on satoshis (integers) as much as possible,
    while using appropriately quantized Decimals when needed.  This class
    wraps around both integer and Decimal amounts appropriately.

    Bitcoin is immutable and the implementation uses an intern pool to
    save memory.
    """

    DECIMAL_PLACES = 8  # minimal unit is 1e-8, a "satoshi"

    # part of Bitcoin interning implementation:
    # weakrefs are used to avoid memory leaks,
    # lock is used for thread safety (maybe not
    # really needed in our use case, due to the GIL)
    __pool = WeakValueDictionary()
    __pool_lock = threading.Lock()

    # prevent the addition of extra attributes,
    # but we do add __weakref__ to allow the usage of weak references
    __slots__ = "satoshis", "decimal", "__weakref__"

    def __new__(cls, value):
        """
        Since Bitcoin is immutable, we need to set its attributes
        in __new__ instead of __init__
        """
        if cls._is_bitcoin(value):
            # no need to copy an immutable
            return value

        try:
            value = cls.quantize(value)
            satoshis = int(value)
            dec = value / 10 ** cls.DECIMAL_PLACES
        except (ValueError, TypeError, InvalidOperation):
            raise BitcoinValueError(
                "Canot create Bitcoin with value '{}' of type {}".format(
                    value, type(value).__name__,
                )
            )

        self = cls.__unintern(satoshis, dec)
        return self

    @classmethod
    def __unintern(cls, satoshis, dec):
        """ retrieve Bitcoin instance with given value """
        with cls.__pool_lock:
            try:
                self = cls.__pool[satoshis]
            except KeyError:
                self = cls.__intern(satoshis, dec)

        return self

    @classmethod
    def __intern(cls, satoshis, dec):
        """ create and cache Bitcoin instance from value """
        self = super().__new__(cls)
        object.__setattr__(self, "satoshis", satoshis)
        object.__setattr__(self, "decimal", dec)
        cls.__pool[satoshis] = self
        return self

    def __setattr__(self, *args):
        raise BitcoinAttributeError("Cannot set attribute on Bitcoin.")

    def __delattr__(self, *args):
        raise BitcoinAttributeError("Cannot delete attribute on Bitcoin.")

    def to_bytes(self, *args, **kwargs):
        """
        Convenience method, since serialization is everywhere in Bitcoin!
        Since the usual format sent over the wire is satoshis encoded
        as bytes, we delegate to the 'satoshis' attribute.
        """
        return self.satoshis.to_bytes(*args, **kwargs)

    def __repr__(self):
        return "Bitcoin('{!s}')".format(self.satoshis)

    def __str__(self):
        return str(self.satoshis)

    @staticmethod
    def _is_bitcoin(operand):
        return isinstance(operand, Bitcoin)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(self.satoshis)

    def __lt__(self, other):
        if self._is_bitcoin(other):
            return self.satoshis < other.satoshis
        return NotImplemented

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

    @classmethod
    def quantize(cls, dec):
        dec = Decimal(dec)
        return dec.quantize(
            Decimal("10") * (-1 * cls.DECIMAL_PLACES), rounding=ROUND_HALF_EVEN
        )

    def __reduce__(self):
        """
        since we made Bitcoin immutable, pickle will have problems
        with re-instantiation; this tells it how to do so
        """
        return Bitcoin, (self.satoshis,)

    def deconstruct(self):
        """
        Needed so Django can write migration files.

        Return a 3-tuple of class import path, positional arguments,
        and keyword arguments.
        """
        module_path = self.__class__.__module__
        class_name = self.__class__.__name__
        import_path = module_path + "." + class_name
        return import_path, (self.satoshis,), {}
