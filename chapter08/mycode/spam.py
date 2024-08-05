import json
import pkgutil


def func():
    # 引数で指定されたリソースを探して byte として返す
    rawdata = pkgutil.get_data(__package__, "resources/data.json")
    textdata = rawdata.decode("utf-8")
    data = json.loads(textdata)
    print(data)


if __name__ == "__main__":
    func()
