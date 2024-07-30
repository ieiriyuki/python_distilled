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

# 7.27 __slots__ によるメモリ効率の向上
# __slots__ はインスタンス変数を __dict__ ではなく配列で保持する
# インスタンスを多数作成する場合にメモリ効率が向上する
# __slots__ にはインスタンスの属性名を指定する
# __slots__ の実装を怠った派生クラスは動作が遅くなり, メモリ使用量が増える
# 多重継承とは両立できない
# __getattribute__ などを再実装する場合は __dict__ がないことに注意する

class Point:
    """point"""
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

p = Point(1, 2)
print(f'Point.__dict__: {p.__dict__}')

class PointSlots:
    """slots"""
    __slots__ = ('x', 'y')
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

p = PointSlots(1, 2)
try:
    print(f'PointSlots.__dict__: {p.__dict__}')
except Exception:
    print('PointSlots.__dict__ is not found')

# 7.28 ディスクリプタ
# オブジェクトの属性にアクセスするときに呼び出されるメソッド
# プロパティはディスクリプタという低レベル構造体を使っている
# クラスレベルでのみインスタンス化できる
# インスタンス単位でディスクリプタを生成することはできない

class Typed:
    expected_type = object

    def __set_name__(self, cls, name):
        """クラスを定義した後, インスタンスが生成される前に呼ばれて
        クラスで使われている名前をディスクリプタに保存する
        """
        self.key = name

    def __get__(self, instance, cls):
        """インスタンスが引数に渡されない場合, ディスクリプタを返す
        __get__ のみを実装したディスクリプタはメソッドディスクリプタと呼ばれる
        弱く束縛される
        メソッドディスクリプタはインスタンス辞書と同じキーが存在しないときに呼ばれる
        属性の遅延評価に使える
        """
        if instance:
            return instance.__dict__[self.key]
        return self

    def __set__(self, instance, value):
        """インスタンスの辞書より優先して参照される"""
        if not isinstance(value, self.expected_type):
            raise TypeError(f'Expected {self.expected_type}')
        instance.__dict__[self.key] = value

    def __delete__(self, instance):
        raise AttributeError('Cannot delete attribute')

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class Account:
    owner = String()
    balance = Float()

    def __init__(self, owner, balance) -> None:
        self.owner = owner
        self.balance = balance

ac = Account('hoge', 100.0)
ac.owner = 'fuga'
try:
    del ac.owner
except Exception as e:
    print(e)

# 遅延評価の例
class Lazy:
    def __init__(self, func):
        self.func = func

    def __set_name__(self, cls, name):
        self.key = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = self.func(instance)
        instance.__dict__[self.key] = value
        return value

class Rectangle:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    area = Lazy(lambda self: self.width * self.height)
    perimeter = Lazy(lambda self: 2 * (self.width + self.height))

r = Rectangle(2, 3)
print(r.__dict__)
print(r.area)
print(r.__dict__)
