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

# 7.23 オブジェクトのライフサイクルとメモリ管理
# クラスインスタンスを作るときに呼び出される __new__ と __init__ の違い

class Foo:
    def __new__(cls, name):
        print(f'__new__ called: {name}')
        self = super().__new__(cls)
        return self

    def __init__(self, name):
        print(f'__init__ called: {name}')
        self.name = name


x = Foo('foo')
repr(x.name)
x = Foo.__new__(Foo, 'bar')
try:
    repr(x.name)
except Exception:
    pass

# https://docs.python.org/ja/3/reference/datamodel.html#basic-customization

# del x や ref count が 0 になったときに __del__ が呼び出される
# __del__ から伝播した例外は無視される
# __del__ でロックやリソースを取得する操作を避けるべき
# __del__ はガベージコレクタによって呼び出されるため, 呼び出されるタイミングは不定

# 7.24 弱参照

import weakref

b = Baz()
r = weakref.ref(b)
print(r)
if x := r():
    print(x.mixin_method())
del b
print(r)

# 弱参照に対応するには, __weakref__ 属性を持つクラスを定義する
# 組み込み型やタプルなどのデータ構造や __slots__ を使っている場合は __weakref__ 属性を持てない
# __slots__ を使っている場合は __weakref__ を __slots__ に追加する
