from decimal import Decimal
from typing import Union

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .bitcoin import Bitcoin


class ModifiedDecimalBaseField(models.DecimalField):
    """Base class for modified versions of DecimalField."""

    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = self.DECIMAL_PLACES  # pylint: disable=no-member
        kwargs['max_digits'] = self.MAX_DIGITS  # pylint: disable=no-member
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['decimal_places']
        del kwargs['max_digits']
        return name, path, args, kwargs


class BitcoinField(ModifiedDecimalBaseField):
    """
    Standardized Decimal representation of money.
    """
    description = _('Bitcoin as a standardized Decimal number.')

    DECIMAL_PLACES = Bitcoin.DECIMAL_PLACES
    MAX_DIGITS = 16

    def from_db_value(self, value, expression, connection, context):  # pylint: disable=unused-argument
        return self.to_python(value)

    def to_python(self, value):
        if value is None or isinstance(value, Bitcoin):
            return value
        try:
            return Bitcoin(value)
        except (TypeError, ValueError):
            raise ValidationError('value {} must be a Decimal or a string representing one.'.format(value))

    def get_prep_value(self, value):
        """
        Prepares value for parameter in query.
        The value type is fairly flexible, but floats are explicitly not allowed.
        """
        if isinstance(value, Bitcoin):
            return value.decimal
        elif type(value) == float:
            raise TypeError("Cannot use float with BitcoinField")
        elif value is None:
            return None
        return Bitcoin(value).decimal

    def get_db_prep_save(self, value, connection):
        """
        Optionally overridden by some model fields, for value types that need
        special handling before saving.  Normally, by default, it just calls
        'get_prep_value' (see above).  DecimalField, in particular,
        uses this to convert a Decimal to the appropriate backend form.

        The difference between DecimalField handling and our handling is that
        the former uses 'to_python' to cast to Decimal whereas we use
        'get_prep_value' to cast; essentially DecimalField needs to upcast
        and we need to downcast.
        """
        value = self.get_prep_value(value)
        return connection.ops.adapt_decimalfield_value(value, self.max_digits, self.decimal_places)
