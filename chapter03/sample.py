import traceback
from contextlib import contextmanager


def some():
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        print(e.__cause__, e.__context__)


some()


class MyContext:
    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, type, val, tb):
        print('exit')
        if type is None:
            print("success")

        print(type, val)
        print("".join(traceback.format_tb(tb)))
        return True


with MyContext() as c:
    print('inside')

with MyContext() as c:
    print('error')
    raise Exception('foo')


@contextmanager
def my_context(iter=3):
    print('start')
    gen = (i for i in range(iter))
    try:
        yield gen
    finally:
        print('end')


with my_context(iter=5) as c:
    for i in c:
        print(i)
