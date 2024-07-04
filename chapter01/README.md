# Pythonの基礎

フォーマット済み文字列は9章で

ビット演算子
```python
<<
>>
&
|
^
~
```
## 1.7 ファイルの入出力

```python
:= # 代入と返り値
print("", file=fp)
open(str, encoding="utf8")
input("prompt: ")
```

## 1.11 辞書

```python
from colections import Counter
```

## 1.14 例外

```python
try:
    do()
except ValueError as e:
    repr(e)
# value error以外が起こるとクラッシュ
```

## 1.15 プログラムの終了

`raise SystemExit("message")`


## 1.16 オブジェクトとクラス

- プログラム中で使われる値は全てオブジェクトです
- `__foo__` は特殊メソッドです
- `_` 1つで始まる名前は慣習としてプライベートとみなす
- `super()` 親クラスのメソッドを呼び出す
- 継承するより合成する

## 1.20 アプリケーションの構成

- 大規模なコードベースを `__init__.py` を含むパッケージにまとめる
