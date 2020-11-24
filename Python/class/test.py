class Singleton(object):
    # __new__はインスタンスが生成する前に呼ばれる
    def __new__(cls, *args, **kargs):
        # hasattrは第一引数のオブジェクトが、第二引数の属性名(文字列)を持っているかを判定
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Myclass(Singleton):
    def __init__(self, input):
        self.input = input


if __name__ == '__main__':
    one = Myclass(1)
    print("one.input={0}".format(one.input))
    two = Myclass(2)
    print("one.input={0}, two.input={1}".format(one.input, two.input))
    one.input = 0
    print("one.input={0}, two.input={1}".format(one.input, two.input))


# class Sandwich:
#     __singleton = None

#     def __new__(cls, *args, **kwargs):
#         if not cls.__singleton:
#             cls.__singleton = super(Sandwich, cls).__new__(cls)
#         return cls.__singleton

#     def set_spam(self, spam=None):
#         self.__spam = spam

#     def get_spam(self):
#         return print(self.__spam)

# sw1 と sw2 は同じものだということがわかる。
# sw1 = Sandwich()
# sw2 = Sandwich()
# sw1.set_spam('spam spam spam')
# sw2.get_spam()
