from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import BigIntegerField
from django.utils.translation import ugettext_lazy as _

from .bitcoin import Bitcoin


HEX_CHARS = "0123456789abcdefABCDEF"


def validate_hex(hex_string):
    if not (len(hex_string) % 2 == 0):
        raise ValidationError(
            "Hex should have even number of characters: %s" % hex_string
        )
    if any(c not in HEX_CHARS for c in hex_string):
        raise ValidationError("Invalid char in hex string: %s" % hex_string)


class HexField(models.CharField):
    description = _("Hex encoding as a string.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validate_hex)


class BitcoinField(BigIntegerField):
    description = _("Bitcoin amount in satoshis.")

    # pylint: disable=unused-argument
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None or isinstance(value, Bitcoin):
            return value
        try:
            return Bitcoin(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "value {} must be an integer or string representing one.".format(value)
            )

    def get_prep_value(self, value):
        """
        Prepares value for parameter in query.
        The value type is fairly flexible, but floats are explicitly not allowed.
        """
        if value is None:
            return None
        if isinstance(value, Bitcoin):
            return value.satoshis
        if type(value) == float:
            raise TypeError("Cannot use float with BitcoinField")
        return Bitcoin(value).satoshis
