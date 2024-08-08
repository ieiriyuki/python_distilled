# 入力と出力

- `bytes`: immutable
- `bytearray`: mutable
- `surrogateescape`: 期待されるエンコーディングに従わないバイトデータでも、エンコード、デコード可能
    - 特定のエンコーディングを保証できない時に有用
- バイト列を渡す方法は、正しくエンコードされていない可能性があるファイルを渡す場合などで有用
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
- `os.scandir`: ディレクトリにあるファイルの一覧
    - `pathlib.Path.glob`: マッチするファイル名を返すジェネレータを返す
    - `pathlib.Path.rglob`: 再起的にファイルを探索

## 9.11 ジェネレータ関数による出力

ファイルオブジェクトに書き込む処理と、出力するオブジェクト生成の処理を分離できる

```python
lines = generator(n)
f.writelines(lines)

# ソケットに書き込む場合
for chunk in lines:
    s.sendall(chunk.encode("utf-8"))
```
