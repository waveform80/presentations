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
        print('Do important stuff')
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
