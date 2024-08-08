a = b"foo"
print(type(a))
c = bytearray()
c.extend(b"world")
print(type(c), c[0])

print("hello".encode("utf-8"))
print(b"hello".decode("utf-8"))


# 9.6 ファイルとファイルオブジェクト
class MyFile:
    def __fspath__(self):
        return "./foo.txt"


with open(MyFile()) as f:
    print(f.read().strip())

from pathlib import Path

p = Path("./foo.txt")
print(p.__fspath__())

# ファイルディスクリプタを扱う場合
import os

fd = os.open("./foo.txt", os.O_RDONLY)
print(fd)
file = open(fd, "rt")  # closefd=False でファイルディスクリプタを閉じない
print(file)
print(file.read().strip())

fout = open("./bar.txt", "wt")
fout.write("aaa")
input(1) # この時点では aaa はファイルに書き込まれていない
fout.flush() # バッファをフラッシュする
# この時点で aaa はファイルに書き込まれている
fout.close()

# 9.11 ジェネレータ関数による出力
fout = open("./generated.txt", "wt")
chunks = []
buffered_size = 0
for _chunk in range(10):
    chunk = f"{_chunk}-"
    chunks.append(chunk)
    buffered_size += len(chunk)
    if buffered_size >= 1000:
        fout.write("".join(chunks))
        chunks.clear()
        buffered_size = 0
fout.write("".join(chunks))
fout.close()

# 9.12 ジェネレータ関数による入力
def line_receiver():
    data = bytearray()
    line = None
    linecount = 0
    while True:
        chunk = yield line  # ジェネレータ関数にデータを渡す
        linecount += chunk.count(b"\n")
        data.extend(chunk)
        if linecount > 0:
            index = data.index(b"\n")
            line = bytes(data[:index + 1])  # 出力対象の行
            data = data[index + 1:]
            linecount -= 1
        else:
            line = None


receiver = line_receiver()
receiver.send(None)
print(receiver.send(b"0"))
print(receiver.send(b"foo\nbar\nbaz\n"))
print(receiver.send(b"1"))
print(receiver.send(b"\n"))
del receiver

print("input by generator")
fin = open("./foo.txt", "r")
r = line_receiver()
data = None
count = 0
while True:
    while not (line := r.send(data)):  # 最初は None なため、データを読み込む
        _bytes = fin.read(1000)
        data = _bytes.encode("utf-8")  # 文字列にしてジェネレータに渡す

    print(line)
    if line.decode().strip() == "baz":
        break
fin.close()

# 9.13
class Serializable:
    def __getstate__(self):
        return {"data": "serialized data"}

    def __setstate__(self, state):
        return {"data": "recovered"}

import pickle

s = Serializable()
filename = "serialized"
pickle.dump(s, open(filename, "wb"))
c = pickle.load(open(filename, "rb"))
print(c)
