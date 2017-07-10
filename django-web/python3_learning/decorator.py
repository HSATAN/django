

def log(func):
    def wrapper(*a,**kwargs):
        print('call %s '%func.__name__)
        print(type(a))
        print(type(kwargs))
        print(kwargs)
        print(kwargs['n'])
        return  func()
    return wrapper

@log
def mydecocrator():
    print('run back')
mydecocrator(a=5)