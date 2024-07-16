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
