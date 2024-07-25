class Countdown:
    def __init__(self, start) -> None:
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1


c = Countdown(3)
for i in c:
    print(i)

print(list(c))

# 6.5 拡張ジェネレータ

def receive():
    print('Ready to receive')
    while True:
        n = yield
        print(f'Received {n}')


r = receive()
r.send(None)
r.send(1)
r.send(2)
r.close()
try:
    r.send(3)
except StopIteration:
    print('Stopped')

try:
    r.throw(ValueError('Invalid value'))  # 廃止予定
except ValueError as e:
    print(f'Error: {e}')

# コンテキストマネージャ
class Manager:
    def __init__(self, gen) -> None:
        self.gen = gen

    def __enter__(self):
        return self.gen.send(None)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                try:
                    self.gen.throw(exc_type(exc_value))
                except exc_type:
                    return False
            else:
                self.gen.send(None)
        except StopIteration as e:
            return True

with Manager(receive()) as r:
    pass

# ローカル変数はクラスやインスタンスの属性より速い
def line_receiver():
    data = bytearray()
    line = None
    count = 0
    while True:
        part = yield line
        count += part.count(b"\n")
        data.extend(part)
        if count > 0:
            index = data.index(b"\n")
            line = bytes(data[:index + 1])
            data = data[index + 1:]
            count -= 1
        else:
            line = None


lr = line_receiver()
lr.send(None)
print(lr.send(b'abc\n'))
print(lr.send(b'hello '))
print(lr.send(b'lovely '))
print(lr.send(b'world\n'))
