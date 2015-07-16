#!/usr/bin/env python

from __future__ import unicode_literals, print_function

# What is an object?
o = object()

# What is a class?
class A(object):
    foo = 2
    bar = 3
    def baz(self):
        return self.foo + self.bar

a = A()
a.__dict__
A.__dict__

# Is a class an object?
a.__class__
A.__class__

# What does the metaclass type do by default?
# Meta(name, parents, attrs)
A.__metaclass__ # not present, so uses "type"

# Equivalent to...
def make_class(**kwargs):
    return type('A', (object,), kwargs)

A = make_class(foo=2, bar=3, baz=lambda self: self.foo + self.bar)
a = A()
a.__dict__
A.__dict__

# Class definition equivalent to:
# MyClass = MyMetaClass.__new__(MyMetaClass, name, parents, attrs)
# MyMetaClass.__init__(MyClass, name, parents, attrs)

# We can see this in action...
class MyMetaClass(type):
    def __new__(meta, name, parents, attrs):
        # attrs['quux'] = 4 # works
        print('__new__')
        print(meta)
        print(name)
        print(parents)
        print(attrs)
        return super(MyMetaClass, meta).__new__(meta, name, parents, attrs)
    def __init__(cls, name, parents, attrs):
        # attrs['quux'] = 4 # doesn't work
        # cls.quux = 4 # works
        print('__init__')
        print(cls)
        print(name)
        print(parents)
        print(attrs)
        super(MyMetaClass, cls).__init__(name, parents, attrs)

class A(object):
    __metaclass__ = MyMetaClass
    foo = 2
    bar = 3
    def baz(self):
        return self.foo + self.bar

a = A()
a.__class__
a.__metaclass__
A.__class__
A.__metaclass__

# What happens when we instantiate an object?
class MyMetaClass(type):
    def __new__(meta, name, parents, attrs):
        print('__new__')
        print(meta)
        print(name)
        print(parents)
        print(attrs)
        return super(MyMetaClass, meta).__new__(meta, name, parents, attrs)
    def __init__(cls, name, parents, attrs):
        print('__init__')
        print(cls)
        print(name)
        print(parents)
        print(attrs)
        super(MyMetaClass, cls).__init__(name, parents, attrs)
    def __call__(cls, *args, **kwargs):
        print('__call__')
        print(args)
        print(kwargs)
        return super(MyMetaClass, cls).__call__(*args, **kwargs)
    def __setattr__(cls, name, value):
        print('__setattr__')
        print(name)
        print(value)
        return super(MyMetaClass, cls).__setattr__(name, value)

class A(object):
    __metaclass__ = MyMetaClass
    foo = 2
    bar = 3
    def baz(self):
        return self.foo + self.bar

a = A()

# A real world example
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
