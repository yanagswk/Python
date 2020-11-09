l = ['good morning', 'god afternoon', 'got night']

print("################")

def greeting():
  yield 'good morning'
  yield 'god afternoon'
  yield 'got night'

for g in greeting():
  print(g)