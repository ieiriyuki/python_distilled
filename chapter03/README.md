# プログラムの構造と制御構造

## 3.3 ループとイテレーション

`for i in s` の `i` のスコープは `for` 文の内部で閉じていません

`zip` は短い方に合わせる。 `strict` オプションでエラーを起こせる

`for ... else ...`

## 3.4 例外

```python
e.args  # 例外が発生した際に渡される引数のタプル
e.__cause__  # 明示的な場合の元々の例外
e.__context  # 暗黙的な場合の元々の例外, 他の例外の処理中に予期しない例外が発生した場合は唯一の情報源となる


class DeviceError(Exception):
    def __init__(self, errno, msg):
        self.args = (errno, msg)
        self.errno = errno
        self.errmsg = msg
```

> 特殊メソッド `__init__()` を再定義するユーザー定義例外の場合、 `__init__()` の引数を含むタプルを上記の例のように `self.args` 属性に代入しておきましょう。 `self.args` は、例外のトレーズバックを表示する際に使われ、 `self.args` 属性が未定義のままだと、エラーが発生した時に例外に関する有益な情報が確認できなくなってしまうからです

`raise SomeError() from e`

```
import traceback

try:
    some()
except Exception as e:
    tblines = traceback.format_exception(e)
    print("".join(tblines))
```

**1つの経験則は、その場で処理すべき手はない例外を補足しないこと**

## 3.5 コンテキストマネージャ

```python
class Sample:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if type is None:
            # ok
        return self
```
