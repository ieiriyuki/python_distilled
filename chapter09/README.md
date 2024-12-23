# 入力と出力

## 9.1 データの表現
- `bytes`: immutable
- `bytearray`: mutable
- `sample.py`

## 9.2 テキストのエンコードとデコード
- `str.encode()`, `str.decode()`
- `surrogateescape`: 期待されるエンコーディングに従わないバイトデータでも、エンコード、デコード可能
    - 特定のエンコーディングを保証できない時に有用
- バイト列を渡す方法は、正しくエンコードされていない可能性があるファイルを渡す場合などで有用

## 9.3 テキストとバイトの書式設定
f string, format, %s

## 9.4 コマンドラインオプション
`sys.argv`, `argparse`, `click`

## 9.5 環境変数
`os`

## 9.6 ファイルとファイルオブジェクト
- `sample.py`
- `open`
- `__fspath__()` が実装されたオブジェクトもファイル名として渡せる
    - `pathlib` を使う際に必要となる
    - `sample.py`
- モード
    - `r`: 読み取り
    - `w`: 書き込み
    - `a`: 追記
    - `x`: ファイルがない時のみ書き込み
    - `+`: 更新モード、読み込みと書き込みができる
- `buffering` 引数でバッファリングを制御できる
    - 0: バッファなし
    - 1: 行単位バッファ
    - 2以上: 指定バイトのバッファ
    - あるプロセスがバッファにデータを書き込んだものの、バッファがフラッシュされなかったために、レシーバがデータを読み込めないことがある
        - デッドロック
        - `flush` すればデータを書き込む
        - `sample.py`
- `errors` にエラー処理を指定できる
- `newline` 引数で改行を指定できる
    - ユニバーサル改行モードで `\n` に変換する

## 9.7 I/O の抽象化層
- `io` クラス
    - `FileIO`
    - `BufferedReader`, `*Writer`, `*Random`
    - `TextIOWrapper`
    - `detach` で IO 抽象化層をデタッチする
- ファイルオブジェクトのメソッド
    - `f.readable`
    - `f.read`, `f.readline`, `f.readlines`
    - `f.readinto(buffer)`: メモリバッファを読み込む, numpy などと組み合わせて使うことが多い
    - `f.writable`
    - `f.write`, `f.writelines`
    - `f.seekable`
    - `f.tell`: 現在のファイル位置
    - `f.seek`: 指定オフセットにファイル位置をシークする
    - `f.isatty`: ターミナルや tty なら True
    - `f.truncate([size])`: ファイルオブジェクトのサイズを最大 size バイトに変更する
    - `f.fileno`: ファイルディスクリプタの値
    - `f.mode`: ファイルモード
    - `f.name`: ファイル名
    - `f.newlines`: 使われている改行文字
    - `f.encoding`
    - `f.errors`: エンコーディングのエラー処理の設定
    - `f.write_through`: バッファリングの有無

## 9.8 標準入力、標準出力、標準エラー
## 9.9 ディレクトリ
- `os.scandir`: ディレクトリにあるファイルの一覧
    - `pathlib.Path.glob`: マッチするファイル名を返すジェネレータを返す
    - `pathlib.Path.rglob`: 再起的にファイルを探索

## 9.10 print() 関数
## 9.11 ジェネレータ関数による出力
## 9.12 ジェネレータ関数による入力
`sample.py`

ファイルオブジェクトに書き込む処理と、出力するオブジェクト生成の処理を分離できる

```python
lines = generator(n)
f.writelines(lines)

# ソケットに書き込む場合
for chunk in lines:
    s.sendall(chunk.encode("utf-8"))
```

## 9.13 直列化
`sample.py`

状態を保持する必要があるオブジェクトを `pickle` するには `__getstate__()` と `__setstate__()` を実装する

`__getstate__()` はオブジェクトの状態を表す値を返す

`__setstate__()` が返す値を使って脱直列化する

脱直列化された先のクラスの用意, 安全性を利用者側が注意する必要がある

## 9.14 ブロッキングと並行処理

- ソケットでノンブロッキング IO を使う場合は `sock.setblocking(False)` にする
- ブロックされた場合 `BlockingIOError` が出る
- IO ポーリング: 例外処理やビジーループに頼らずにデータの有無を確認できる
    - `select` や `selectors` モジュールを使う

```python
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

def run(sock1, sock2):
    selector = DefaultSelector()
    selector.register(sock1, EVENT_READ, data=func1)
    selector.register(sock2, EVENT_READ, data=func2)
    while True:
        for key, evt in selector.select():
            func = key.data
            func(key.fileobj)
```

スレッドを使う場合

```python
import threading

t1 = threading.Thread(target=func1, args=[])
t2 = threading.Thread(target=func2, args=[])
t1.start()  # スレッド開始
t2.start()
t1.join()  # 完了待ち
t2.join()
```

`asyncio`

```python
import asyncio

async def func1():
    pass

async def func2():
    pass

async def main():
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(func1())
    t2 = loop.create_task(func2())
    await t1
    await t2

asyncio.run(main())
```

## 9.15 I/O 標準ライブラリ

- `asyncio`: `asyncio_sample.py`
- `binascii`: `binascii_sample.py`
- `configparser`
- `csv`
- `errno`: エラーの番号を検証する
    - `except OSError as e: e.errno == errno.ENOSPC`
- `fcntl`

```python
import fcntl  # unix 上で fcntl や ioctl システムコールを使って低レベルの IO 制御をする
# 並行処理や分散システムでロックをする時にも使う
with open("somefile", "r") as file:
    try:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
    finally:
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
```

- `http`: `python -m http.server`
- `io`: ファイルオブジェクトをなんやかんやできる
- `json`
- `logging`
- `os` もあるけど `pathlib` の方が便利
- `re`
- `shutil`: シェル操作
- `select`: 複数の IO ストリームの単純なポーリング
- `smtplib`: メールのクライアントライブラリ, `smtplib_sample.py`
- `socket`: `socket_*.py`
- `struct`: python とバイナリデータ構造の間でデータの交換を行う
- `subprocess`: `run` で結果を受け取れる
- `tempfile`
- `textwraps`
- `threading`: https://docs.python.org/ja/3.12/library/threading.html
    - daemon フラグでデーモンモードになる
    - スレッドを終了させたい場合は、フラグ変数などを明示的に作って制御する
    - 共有データを操作する場合は `Lock` を使う
    - 別のスレッドの処理を待つ場合は `Event` を使う
    - スレッド同士が通信する場合は `Queue` を使う
- `time`
- `urllib`: ごく簡単な操作でなければ `requests` や `httpx` を使うべき
- `unicodedata`: ノーマライズしたり、プロパティ調べたり
- `xml`: `from xml.etree.ElementTree import ElementTree; doc = ElementTree(file="recipe.xml")` で基本的な読み取りができる
