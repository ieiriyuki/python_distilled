# モジュールとパッケージ

- モジュールはキャッシュされるため、2度インポートしても変更は反映されない
- `from module import name` でもモジュール全体をインポートする
- `__all__` で `import *` の対象を管理できる
- インポートしたモジュールのリロードやアンロードに信頼できる方法はない
- デプロイやパッケージングにおいて `__pycache__` のようなバイトコードを含めると、プログラムが速くなる面もある
- `exec()` など動的なコード生成やメタプログラミングを使うと遅くなる e.g. `@dataclass`
- `sys.path` の操作や、 `PYTHONPATH` 環境変数で検索ディレクトリを追加できる
- `__main__.py` がある **ディレクトリ** を実行すると `__main__.py` を実行する
- `__init__.py` がなくても Pythonファイルがあるディレクトリを名前空間パッケージとして使える
- 名前空間パッケージはほとんど使わない
- `__init__.py` にサブモジュールをインポートして名前空間を管理する

# 8.14 パッケージのリソース

`pkgutil.get_data(package, resource)` でデータを読み込む

```bash
mycode/
  resources/
    data.json
  __init__.py
  spam.py
  yow.py
```

```python
# mycode/spam.py
import json
import pkgutil

def func():
    # 引数で指定されたリソースを探して byte として返す
    rawdata = pkgutil.get_data(__package__, "resources/data.json")
    textdata = rawdata.decode("utf-8")
    data = json.loads(textdata)
```

- オブジェクト
    - `__name__`: 完全修飾モジュール名
    - `__file__`: 定義されたファイル名
    - `__package__`: 上位モジュールの名前
    - `__path__`: サブモジュールを検索するためのサブディレクトリのリスト
    - `__annotations__` モジュールレベルの型ヒント
- https://packaging.python.org/ja/latest/tutorials/packaging-projects/
- コードを自己完結型のプロジェクトとして分離しておくこと

```python
# setup.py
from setuptools import setup

setup(
    name="spam",
    version="0.0",
    pacakges=["spam"],
    scripts=["runspam.py"],
)
```
