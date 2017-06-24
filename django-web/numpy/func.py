import numpy
def ulti(a):
    result=numpy.zeros_like(a)
    result.flat=42
    return result

#ufunc=numpy.frompyfunc(ulti,1,1)
#print(ufunc(numpy.arange(3)))

import time
import datetime
strt='2017-06-14 15:31:53'
print(str(strt.split(' ')[0]))
#print(datetime.datetime(str))