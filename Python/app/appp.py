



class App:

  def __init__(self, a, b):
    self.aaaa = a + b 
    self.xxxx = a * b
  

  def tashizan(self, a, b):
    aaaa = self.aaaa * a
    xxxx = self.xxxx * b
    return aaaa + xxxx


AAAA = App(1, 2).tashizan(2, 3)

# print(AAAA)
