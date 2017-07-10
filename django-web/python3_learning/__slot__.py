class myslot():
    __slot__=('print_name',)
    def __test(self):
        print('test')
    def get_test(self):
        self.__test()
def print_name(name):
    print(name)

shili=myslot()
shili.print_name1=print_name

shili.print_name1('huangkaijie')
shili.get_test()