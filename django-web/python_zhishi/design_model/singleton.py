# -*- coding:utf-8 -*-
class SingleTon(object):
    __instance=None
    def __init__(self):
        self.id=1
        pass

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self._instance = super(SingleTon, self).__call__(*args, **kwargs)
        return self._instance
class SingleTon2(object):
    __instance=None
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=super(SingleTon2,cls).__new__(cls)
        return cls.__instance
if __name__=="__main__":
    print(SingleTon())
    print(SingleTon().id)
    print(SingleTon2())
    print(SingleTon2() is SingleTon2())
    print(SingleTon2())
    print(SingleTon2())
    print(SingleTon2())
    print(SingleTon2())