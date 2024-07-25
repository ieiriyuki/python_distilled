# ジェネレータ

## 6.1 ジェネレータと yield　文

ジェネレータ関数に対してクリーンアップが必要ならば、 `try-finally` やコンテキストマネージャを使う

```python
def countdown(n):
    print("start", n)
    try:
        while n > 0:
            yield n
            n -= 1
    finally:
        print("end at", n)

def func(file):
    with open(file) as f:
        yield data
    # done
```

## 6.3 ジェネレータの委譲

`yield from`

```python
def flatten(items):
    for i in items:
        if isinstance(i, list):
            yield from flatten(i)
        else:
            yield i
```
## 6.4 ジェネレータの実例

```python
# 再帰数制限に対応する
def flatten(items):
    stack = [iter(items)]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, list):
                stack.append(iter(item))
            else:
                yield item
        except StopIteration:
            stack.pop()
```

