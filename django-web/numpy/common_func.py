import numpy as np
import sys
fb=r'E:\django-git\django\django-web\numpy\Code\ch4code\ch4code\BHP.csv'
fv=r'E:\django-git\django\django-web\numpy\Code\ch4code\ch4code\VALE.csv'
c,v=np.loadtxt(fb,delimiter=',',usecols=(6,7),unpack=True)
vale=np.loadtxt(fv,delimiter=',',usecols=(6,),unpack=True)
change=np.diff(c)
print(change)
symbol=np.sign(change)
piece=np.piecewise(change,[change>0,change<0],[9,-9])
print(symbol)
print(v)
print(v[1:]*symbol)
print(symbol>0)
o, h, l, c = np.loadtxt(fb, delimiter=',', usecols=(3, 4, 5, 6), unpack=True)
def calc_profit(open, high, low, close):
    # 在开盘时买入
    buy = open * float(1)
    # 当日股价区间
    print(low,buy,high)
    if low < buy < high:
        return (close - buy)/buy
    else:
        return 0
func = np.vectorize(calc_profit)
profits = func(o, h, l, c)
print ("Profits", profits)