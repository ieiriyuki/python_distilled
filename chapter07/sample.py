# 7.17 プロパティ

class Foo:
    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value

    @foo.deleter
    def foo(self):
        del self._foo


f = Foo()
f.foo = 1
print(f.foo)
del f.foo
try:
    print(f.foo)
except AttributeError as e:
    print(f'Error: {e}')

# 7.19 ミックスイン

class Mixin:
    def mixin_method(self):
        return super().mixin_method()

class Bar:
    def mixin_method(self):
        return 'bar_method'

class Baz(Mixin, Bar):
    pass


baz = Baz()
print(baz.mixin_method())
