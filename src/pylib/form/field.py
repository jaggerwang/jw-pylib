from collections import OrderedDict
import re
from copy import copy
from datetime import datetime
import json

from bson import ObjectId
from bson.errors import InvalidId
from wtforms import Field


class StringField(Field):

    def __init__(self, label=None, validators=None, empty_to_default=True,
                 strip=True, words_filter=None, no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.strip = strip
        self.words_filter = words_filter
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0]

            if self.strip:
                value = value.strip()

            if self.words_filter:
                value = self.words_filter.filter(value)

            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                self.data = value
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class IntegerField(Field):

    def __init__(self, label=None, validators=None, empty_to_default=True,
                 no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = int(value)
                except ValueError:
                    self.data = None
                    raise ValueError("invalid int: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class FloatField(Field):

    def __init__(self, label=None, validators=None, empty_to_default=True,
                 no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = float(value)
                except ValueError:
                    self.data = None
                    raise ValueError("invalid float: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class BooleanField(Field):

    def __init__(self, label=None, validators=None, false_values=('false', '0'),
                 empty_to_default=True, no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.false_values = false_values
        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                self.data = False if value in self.false_values else True
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class DateTimeField(Field):

    def __init__(self, label=None, validators=None,
                 format='%Y-%m-%d %H:%M:%S', empty_to_default=True,
                 tzinfo=None, no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.format = format
        self.empty_to_default = empty_to_default
        self.tzinfo = tzinfo
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = datetime.strptime(value, self.format)
                    if self.tzinfo:
                        self.data = self.data.replace(tzinfo=self.tzinfo)
                except ValueError:
                    self.data = None
                    raise ValueError("invalid datetime: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class DateField(Field):

    def __init__(self, label=None, validators=None, format='%Y-%m-%d',
                 empty_to_default=True, no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.format = format
        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = datetime.strptime(value, self.format).date()
                except ValueError:
                    self.data = None
                    raise ValueError("invalid datetime: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class ObjectIdField(Field):

    def __init__(self, label=None, validators=None, empty_to_default=True,
                 no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = ObjectId(value)
                except InvalidId:
                    self.data = None
                    raise ValueError("invalid ObjectId: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class TagListField(Field):

    def __init__(self, label='', validators=None, sep=",，、",
                 empty_to_default=True, element_field=None, unique=True,
                 no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.sep = sep
        self.empty_to_default = empty_to_default
        self.element_field = element_field
        self.unique = unique
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                value = [v.strip() for v in re.split(
                    r"[{}]".format(self.sep), value)]

                value = [v for v in value if v != ""]

                if self.unique:
                    value = list(OrderedDict.fromkeys(value))

                self.data = value
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None

    def post_validate(self, form, stop_validation):
        if stop_validation:
            return

        if self.data is not None and self.element_field is not None:
            fields = []
            for v in self.data:
                field = copy(self.element_field).bind(form, '')
                field.process_formdata([v])
                if not field.validate(form):
                    self.errors.extend(field.errors)
                else:
                    fields.append(field)

            if len(self.errors) == 0:
                self.data = [v.data for v in fields]


class JsonField(Field):

    def __init__(self, label=None, validators=None, empty_to_default=True,
                 no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                try:
                    self.data = json.loads(value)
                except ValueError:
                    self.data = None
                    raise ValueError("invalid json: '{}'"
                                     .format(values[0]))
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None


class CompoundField(Field):

    def __init__(self, label='', validators=None, empty_to_default=True,
                 fields=None, no_to_default=True, **kwargs):
        super().__init__(label, validators, **kwargs)

        self.empty_to_default = empty_to_default
        self.fields = fields or []
        self.no_to_default = no_to_default

    def process_formdata(self, values):
        if values:
            value = values[0].strip()
            if value == "":
                self.data = self.default if self.empty_to_default else ""
            else:
                self.data = value
        else:
            if self.no_to_default:
                self.data = self.default
            else:
                self.data = None

    def post_validate(self, form, stop_validation):
        if stop_validation:
            return

        if self.data is not None:
            for field in self.fields:
                field = field.bind(form, '')

                try:
                    field.process_formdata([self.data])
                except ValueError as e:
                    self.errors.append(str(e))
                    continue

                if not field.validate(form):
                    self.errors.extend(field.errors)
                else:
                    self.data = field.data
                    self.errors = []
                    break
