class Cookies():
    max_cookie = 2
    current_cookie = 0
    def __new__(cls):
        if cls.current_cookie >= cls.max_cookie:
            raise ValueError('すでに２つクッキーがあるので新しいクッキーは作りません')
        cls.current_cookie += 1
        return super().__new__(cls)  # いつも通り普通にクッキーを作ってねという命令


my_cookie = Cookies()
your_cookie = Cookies()
nobita_cookie = Cookies()  # すでに２つクッキーがあるので...と出る
print(nobita_cookie)  # => name 'nobita_cookie' is not defined