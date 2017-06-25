#coding=utf-8
import numpy
from matplotlib import pyplot
from scipy import misc
p1=misc.imread(r'C:\Users\edison\Desktop\1.jpg')
p2=misc.imread(r'C:\Users\edison\Desktop\2.jpg')
print(type(p1))
print(p1.shape,p1.dtype)
print(p2.shape,p2.dtype)
p=(p1*0.5)+(p2*0.5)
#pyplot.imshow(p)
#p1.flat=0
p1=p1[400:,200:300,0]
#pyplot.show()
l=misc.ascent()
#misc.imsave('lena.png',l)
pyplot.imshow(p1)
pyplot.show()