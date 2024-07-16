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

