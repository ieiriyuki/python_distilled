# クラスとオブジェクト指向プログラミング

## 7.8 継承より合成

デリゲーションと同じ

dependency injection と同じこと

## 7.9 継承よりも関数

メソッドを1つしか持たないクラスをいくつも書くのであれば, 関数を使うべき

某ソナーで小さいクラスいっぱい作ったな...

## 7.11 組み込み型の継承の危険性

Python の組み込み型は C 言語で実装されている

組み込み型のメソッドは C 言語の世界で動く

`collections.UserDict` などを使う

とはいえそもそも継承するべきではない

## 7.12 クラス変数とクラスメソッド

クラスメソッドの一般的な使い方はコンストラクタの代替を定義すること

コンストラクタのようなメソッドの命名規則として `from` で始めることが多い

## 7.13 静的メソッド

たまたまクラス内で定義した通常の関数

```python
class Foo:
    @staticmethod
    def add(x, y):
        return x + y
```

**概念を別のクラスに切り出す**

バリューオブジェクト的な, DDD的な

`@staticmethod` を使うべき理由として, メソッドを作るだけで, インスタンスを生成する必要がないこと

## メモ

TypeScript では型チェックってどうなっているんだろう

コンパイルする時だけ?

実行時に意図しない型がきても動いちゃう?

## 7.19 多重継承, インターフェース, ミックスイン

一般的に多重継承は型とインターフェースの関係を整理する際に使います

ミックスインクラスは、単独では使わず、他のクラスと組み合わせて使う

メソッド解決順序
- `__mro__` で確認できる
- 派生クラスは基底クラスよりも先にチェックする
- 継承順に検索する
- C3線型化アルゴリズム
- 派生クラスは基底クラスより先に記載する
- ミックスインの実装では、全て同一の関数シグネチャを持たせるようにする (chapter 5)
    - 同じ仮引数ってことかな
- 常に `super()` を使う

## 7.20 型ベースディスパッチ

型に応じて処理を変えるやつ

- `if-else` : ugly
- `dict` : `for ty in type(obj).__mro__: dict.get(ty)` する必要あるかも
- `getattr` : dict のを getattr 使うように変える感じ
- pattern match : new in 3.10

## 7.21 クラスデコレータ

```python
_registory = {}

def register_decoder(cls):
    for mt in cls.mimetypes:
        _registory[mt] = cls
    return cls

@register_decoder
class TextDecorder:
    mimetypes = ["text/plain"]

    def decode(self, data):
        pass
```

既存のメソッドを書き換えることができる

ミックスインや多重継承の代わりによく使う

デコレータが適用されるときに `cls.noise` が1度だけ実行されるため、ミックスインより速い

```python
def loud(cls):
    org_noise = cls.noise

    def noise(self):
        return org_noise(self).upper()

    cls.noise = noise
    return cls

@loud
class Cyclist:
    def noise(self):
        return "cycle"
```

ユーティリティなメソッドをいちいち実装するよりデコレータで付与する

see `sample.py`

`exec` で動的にコードを生成すると, Python がモジュールに適用するコンパイル最適化の恩恵を受けられない

この方法で大量にクラスを定義すると, コードのインポートが著しく遅くなる可能性がある

## 7.25 内部オブジェクトの表現と属性束縛

- `__dict__`
- `__class__`
- `__bases__`
- `__mro__`

## 7.26 プロキシ, ラッパ, 委譲

- プロキシ: 他のオブジェクトと同じインターフェースを持つオブジェクト
- 一般的なプロキシの実装には `__getattr__()` を使う
- 特殊メソッドを利用するには明示的に実装する
    - `len` なら `__len__()`
    - `append` なら `__setitem__()`

e.g.
```python
class A:
    def spam(self):
        print("A.spam")

    def grok(self):
        print("A.grok")

    def yow(self):
        print("A.yow")

class LoggedA:
    def __init__(self):
        self._a = A()

    def __getattr__(self, name):
        print("Accessing", name)
        return getattr(self.a, name)
```
