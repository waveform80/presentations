class Field(object):
    _counter = 0
    _type = 'text'

    def __init__(self, *args):
        super(Field, self).__init__()
        Field._counter += 1
        self._counter = Field._counter

    def render(self):
        assert self._name is not None
        return '<input type="%s" name="%s">' % (self._type, self._name)

TextField = Field

class IntegerField(Field):
    _type = 'int'

class DateField(Field):
    _type = 'datetime-local'

class BooleanField(Field):
    _type = 'checkbox'

class DecimalField(Field):
    _type = 'float'


class FormMeta(type):
    def __init__(cls, name, parents, attrs):
        fields = []
        for name in attrs:
            field = getattr(cls, name)
            if not name.startswith('_') and isinstance(field, Field):
                field._name = name
                fields.append(field)
        cls._fields = sorted(
                fields, key=lambda field: (field._counter, field._name))
        super(FormMeta, cls).__init__(name, parents, attrs)


class Form(object):
    __metaclass__ = FormMeta

    def render(self):
        for field in self._fields:
            print(field.render())
