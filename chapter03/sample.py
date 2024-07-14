def some():
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        print(e.__cause__, e.__context__)


some()
