a = [i for i in range(5)]
print(a)


def foo(items):
    for i, v in enumerate(items):
        items[i] = v + 1
    return sum(items)


print(foo(a), a)


# 5.15 高階関数
def make_greetings(names):
    funcs = []
    for name in names:
        funcs.append(lambda: print("Hello " + name))
    return funcs


a, b, c = make_greetings(["a", "b", "c"])
a()  # Hello c
b()  # Hello c
c()  # Hello c

# 変数のコピーを保持したい場合はデフォルト引数として渡す
def make_greetings(names):
    funcs = []
    for name in names:
        funcs.append(lambda name=name: print("Hello " + name))
    return funcs


a, b, c = make_greetings(["a", "b", "c"])
a()  # Hello a
b()  # Hello b
c()  # Hello c


# 5.16 コールバック関数における引数の受け渡し
import time


def after(seconds, callback):
    time.sleep(seconds)
    callback()


def add(x, y):
    print(x + y)
    return x + y


try:
    after(3, add(3, 4))
except TypeError as e:
    print(e)


after(3, lambda: add(3, 4))  # 引数を持たない関数を thunk と呼ぶ

from functools import partial  # 指定された1つ以上の引数を固定した新しい関数を返す

after(3, partial(add, 3, 4))

# 参考
def f(x, y, z):
    return x + y + z

# カリー化: 複数の引数を取る関数を, 1つの引数を取る関数の連続に変換すること
# カリー化は一般的な Python のスタイルではない
def fc(x):
    return lambda y: lambda z: x + y + z

# 安全な引数の渡し方の例
def after(seconds, func, debug=False, /, *args, **kwargs):
    time.sleep(seconds)
    if debug:
        print(f"Waiting {seconds} seconds")
    func(*args, **kwargs)


# 5.17 コールバック関数の返り値
# その例外は何に起因するのか?
# after("1", add, 3, 4)  # TypeError in after
# after(1, add, False, "3", 4)  # TypeError in add

# 1. 個別の例外として処理する
class CallbackError(Exception):
    pass


def after(seconds, func, debug=False, /, *args, **kwargs):
    time.sleep(seconds)
    if debug:
        print(f"Waiting {seconds} seconds")
    try:
        func(*args, **kwargs)
    except TypeError as e:
        raise CallbackError("callback failed") from e


try:
    after(1, add, False, "2", 3)
except Exception as e:
    print(f"{e}")


# 2. 返り値とエラーを両方返す
# go とか rust っぽい
# python だと concurrent.futures.Future
class Result:
    def __init__(self, value=None, exc=None):
        self._value = value
        self._exc = exc

    def result(self):
        if self._exc:
            raise self._exc
        return self._value


def after(seconds, func, *args):
    time.sleep(seconds)
    try:
        return Result(value=func(*args))
    except Exception as e:
        return Result(exc=e)


res = after(1, add, "2", 3)
try:
    res.result()
except Exception as e:
    print(f"{e}")


import inspect

print(inspect.signature(print))
