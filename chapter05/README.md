# 関数

## 5.7 位置専用引数

https://atsuoishimoto.hatenablog.com/entry/2019/09/06/115651

## 5.8 名前, ドキュメンテーション文字列, 型ヒント

- https://gihyo.jp/article/2022/09/monthly-python-2209
- https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
- https://microsoft.github.io/pyright/#/
    - https://future-architect.github.io/articles/20220301a/

## 5.9 副作用のある関数

ミュータブルを引数に渡すと, 意図しない副作用が起こる可能性がある

副作用のあるコードでは `None` を返すようにする

## 5.10 返り値

https://docs.python.org/ja/3/library/typing.html#typing.NamedTuple

## 5.11 スコープルール

- ローカル名前空間
- グローバル名前空間
- `global` 文の使用は悪いスタイル, クラスを使う
- ネスト垂れた関数内の変数はレキシカルスコープで束縛される
- `nonlocal`

## 5.14 `lambda` 式

遅延束縛

```python
x = 2
f = lambda y: x * y
x = 3
g = lambda y: x * y
print(f(10))  # 30
print(g(10))  # 30
```

## 5.18 デコレータ

`functools.wraps()` を使う

```python
def trace(func):
    @wraps(func)
    def call(*args):
        return func(*args)
    return call


@classmethod # 最後=外側
@decorate # 最初=内側
def func(): pass

# 引数を受け取る場合
def trace(message):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorate  # デコレータを返す

# イベントハンドラの例
_event_handlers = {}
def eventhandler(event):
    def register_function(func):
        _event_handlers[event] = func
        return func
    return register_function

@eventhandler("BUTTON")
def handle_button(msg): pass
```

## 5.19 map, filter, recude

https://docs.python.org/ja/3/library/functools.html#functools.reduce

## 5.20 イントロスペクション, 属性, シグネチャ

- `f.__name__`: 関数名
- `f.__qualname__`: モジュールへのパスの情報を含む完全修飾名
- `f.__module__`: モジュール名
- `f.__globals__`: 関数のグローバル名前空間として使う辞書
- `f.__doc__`: ドキュメンテーション文字列
- `f.__annotations__`: 型ヒント
- 関数の仮引数を知りたいときは `inspect.signature()` を使う
- シグネチャ: 関数の性質を記述するメタデータ
- `f.__signature__` にシグネチャオブジェクトを保存することができる
