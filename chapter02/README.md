# 演算子、式、データ操作

# 2.7 論理式と真偽値

論理式を検証する場合は常に正確を期すこと

```python
def f(x, item=None):
    if not item:  # 不適切
        item = []
    item.append(x)
    return item
```

## 2.9 イテラブルオブジェクト

https://docs.python.org/ja/3/library/collections.abc.html

## 2.10 シーケンス

浅いコピー

```python
a = [3, 4, 5]
b = [a]  # 浅いコピー
c = 4 * b
[[3, 4, 5], [3, 4, 5], [3, 4, 5], [3, 4, 5]]
a[0] = -7  # c も変わる
```

スライス
```python
first_five = slice(0, 5)
s = "hello world"
s[firsr_five]
```

https://docs.python.org/ja/3/library/copy.html

## 2.11 ミュータブルシーケンス

> スライス代入はオプションでストライド引数を渡せます。ストライド引数を追加した場合、代入する値は置換されるスライスと同じ要素を持つ必要があります。

## 2.12 Set

`s.remove(x)` x を削除する。なければエラー

`s.discard(x)` x を削除する。

## 2.15 ジェネレータ式

結果をその都度返す

`squares = (x * x for x in items)`

## 2.18 演算の評価順序

上ほど優先

- `x & y`
- `x ^ y`
- `x | y`
- `x < y` 他
- `not x`
- `x and y`
- `x or y`
