
# 関数呼び出しの時に、前後で何か処理をしたい時にデコレーターを使う。

# print_info関数のように、一度デコレーターを記述してしまえば、違う関数が出てきたときに同様の処理が書ける。

def print_more(func):
  def wrapper(*args, **kwargs):
    print('func:', func.__name__)
    print('args:', args)
    print('kwargs:', kwargs)
    result = func(*args, **kwargs)
    print('result:', result)
    return result
  return wrapper

def print_info(func):
  def wrapper(*args, **kwargs):
    print('start')
    result = func(*args, **kwargs)
    print('end')
    return result
  return wrapper


@print_info
@print_more
def add_num(a, b):
  return a + b

@print_info
def sub_num(a, b):
  return a - b


r = add_num(10, 20)
print(r)
# r = sub_num(10, 20)
# print(r)

