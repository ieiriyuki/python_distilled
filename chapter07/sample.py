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

# 7.21 クラスデコレータ
import inspect

def with_repr(cls):
    args = list(inspect.signature(cls).parameters)
    argvals = ", ".join("{self.%s!r}" % arg for arg in args)
    code = "def __repr__(self):\n"
    code += f'    return f"{cls.__name__}({argvals})"\n'
    locs = {}
    exec(code, locs)
    cls.__repr__ = locs["__repr__"]
    return cls

@with_repr
class Point:
    def __init__(self, x, foo):
        self.x = x
        self.foo = foo

print(Point(1, 2))

# 7.22 継承のチェック
# __init__subclass__ を基底クラスに実装する
class DecoderBase:
    _registory = {}

    @classmethod
    def __init_subclass__(cls, **kwargs):
        for mt in cls.mime_types:
            DecoderBase._registory[mt] = cls
        # 多重継承する場合は super().__init_subclass__(**kwargs) を呼び出す

class JSONDecoder(DecoderBase):
    mime_types = ['application/json']

    def decode(self, data: str):
        print(data)

DecoderBase._registory["application/json"]().decode('hi')
