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

## 2.10 シーケンス

浅いコピー
