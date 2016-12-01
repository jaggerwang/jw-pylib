from wtforms import ValidationError
from wtforms.validators import Regexp

from ..string import display_width


def DisplayWidth(min_width=None, max_width=None, length_counter=display_width):

    def _validate(form, field):
        if field.data is None:
            return

        width = length_counter(field.data)

        if min_width is not None and width < min_width:
            raise ValidationError(
                "too short: {} < {}".format(width, min_width))

        if max_width is not None and width > max_width:
            raise ValidationError("too long: {} > {}".format(width, max_width))

    return _validate


def TagLength(max_number=None, min_len=None, max_len=None, anyof=None):

    def _validate(form, field):
        if field.data is None:
            return

        number = len(field.data)
        if max_number is not None and number > max_number:
            raise ValidationError(
                "too many tags: {} > {}".format(number, max_number))

        for v in field.data:
            width = len(v)

            if min_len is not None and width < min_len:
                raise ValidationError("tag '{}' too short: {} < {}"
                                      .format(v, width, min_len))

            if max_len is not None and width > max_len:
                raise ValidationError("tag '{}' too long: {} > {}"
                                      .format(v, width, max_len))

            if anyof is not None and v not in anyof:
                raise ValidationError("tag '{}' not in {}"
                                      .format(v, anyof))

    return _validate


class Version(Regexp):

    def __init__(self, message=None):
        super().__init__(r'^\d{1,2}(?:\.\d{1,2})?(?:\.\d{1,2})?$', 0, message)

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('Invalid version.')

        super().__call__(form, field, message)


class Section3Version(Regexp):

    def __init__(self, message=None):
        super().__init__(r'^\d{1,2}\.\d{1,2}\.\d{1,2}$', 0, message)

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('Invalid version.')

        super().__call__(form, field, message)
