
# def fn(*args, **kwargs):
#   print('*args:', args)
#   print('**kwargs', kwargs)

# fn(11, 'aa', ['ラーメン', '巣ドン'])
# fn(key1=22, key2="bb", key3=["パスタ", "スープ"])
# fn(11, "aa", key1=22, key2="bb")



def sample(p1, p2):
  print('p1=', p1)
  print('p2=', p2)

params = [111, "AAA"]
sample(*params)

