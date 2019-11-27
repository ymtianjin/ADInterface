# encoding=utf-8

# 自定义异常
class CheckElementException(Exception):  # 自定义异常类，继承exception

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AssertException(Exception):  # 自定义异常类，继承exception

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
