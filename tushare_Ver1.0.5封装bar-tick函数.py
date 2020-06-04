# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:08:30 2017

@author: zack zhang
"""
import os
import pandas as pd
from pandas import Series
from pandas import DataFrame as df
import tushare as ts
import datetime
import time
from collections import OrderedDict
from decimal import getcontext, Decimal
from threading import Timer

cons = ts.get_apis()
Today = datetime.date.today().strftime("%Y-%m-%d")
TenDaysAgo = (datetime.date.today() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")
print '当前是否A股交易时间：' , 92959 < int(time.strftime("%H%M%S")) < 145959
print '当前是否港股交易时间：' , 92959 < int(time.strftime("%H%M%S")) < 160959
print '当前是否商品期货交易时间：' , 205959 < int(time.strftime("%H%M%S")) < 235959 \
                                   or 0 < int(time.strftime("%H%M%S")) < 23000 \
                                   or 85959 < int(time.strftime("%H%M%S")) < 145959
#df1 = ts.bar('000729', conn=cons, freq='D', asset='E', start_date=TenDaysAgo, end_date='', adj = 'qfq')#bar没用market参数也可以
#print df1.head(5)
#print ts.get_markets(xapi=cons)
#print "#"*50
#df2 = ts.tick('03188', conn=cons, date=Today, asset='X')#.iat[-1,3]/1000 #, market='KH', retry_count = 3
#print df2.tail(5)

#print df2.iat[-1,3] #48550
#print df2.iat[-1,3]/1000 #应为48.55但直接显示为48
#print round(df2.iat[-1,3]/1000,2) #round不起作用，仍为48.0
#print float('%.2f' % (df2.iat[-1,3]/1000)) #不起作用，仍为48.0
#print Decimal(str(df2.iat[-1,3]/1000)).quantize(Decimal('0.00')) #不起作用，仍为48.00
#print Decimal.from_float(48550/1000).quantize(Decimal('0.000')) #不起作用，仍为48.000
#print 48550/1000 #python为整除=48
#print 48550/1000.0 #分子分母任一为浮点数则结果为浮点数48.55而非为整除=48！
'''
bar函数参数：
1、沪深股票（0、3、6）开头的六位数字可用adj = 'qfq'前复权参数，asset='E'，end_date=''则开盘时间内显示T-1日K线bar；
2、沪深场内基金（1、5）开头的六位数字不可用adj = 'qfq'前复权参数，asset='E'，end_date=''则开盘时间内显示当日实时bar价格；
3、港股、香港ETF(0)开头的五位数字可用adj = 'qfq'前复权参数，asset='X'，end_date=''则开盘时间内显示当日实时bar价格；
4、国内商品期货（字母）开头+四位数字可用adj = 'qfq'前复权参数，asset='X'，end_date=''则开盘时间内显示当日实时bar价格,
   另外商品期货也有结算价数据，但次日价格是和T-1收盘价连续的，因此结算价对日内走势判断意义不大。
'''
'''
tick函数返回的DataFrame格式的“时间”、“价格”列分别如下：
1、A股股票(601888) = df[['datetime','price']].tail(5), 列数为1、2，价格小数点后2位；
2、沪深场内ETF(510300) = [['datetime','price'/10]].tail(5), 列数为1、2，价格小数点后3位；
3、港股股票(00700) = [['date','vol'/1000]].tail(5), 列数为1、3，价格小数点后2位；
4、国内商品期货(rb1805,P1805,FG1805) = [['date','vol'/1000]].tail(5), 列数为1、3，价格整数（？）；
5、香港ETF(03188) = [['date','price'/1000]].tail(5), 列数为1、4，价格小数点后2位；
'''

path = os.path.abspath(os.path.dirname(__file__))
Rics = pd.read_csv(path+'\Rics.csv',low_memory=False)
Rics = Rics.applymap(lambda x: x.replace(',','') )

format1 = lambda x: '0'+x if x.endswith('.HK') else x
format2 = lambda x: x.replace('.SH','').replace('.SZ','').replace('.HK','')
TsSymbol = Rics['Ric'].map(format1).map(format2)
format3 = lambda x: round(x,3)
#TsSymbol = Series(TsSymbol)  
#print TsSymbol
def PreClose(L):
    '''
    此函数最好当日收盘后一次性跑完存入csv文件，以备第二天盘中读取使用，
    不要在第二天盘中跑，因盘中沪深场内基金、港股及香港ETF、期货用此函数读取的第一行是实时K-bar
    '''
    ClosePrice = OrderedDict()#此处应用sortdic,不然dic的k, v顺序会乱
    for i in L:
        if i.isdigit() and len(i) == 6:
            if i.startswith('1') or i.startswith('5'):#沪深场内基金
                if 92959 < int(time.strftime("%H%M%S")) < 145959:#如果在交易时间内，取close列第二行
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                    asset='E').close[1]
                else:
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                    asset='E').close[0]
            else:#0,3,6开头六位沪深股票
                ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                 asset='E', adj = 'qfq').close[0]            
        else:
            if i.isdigit() and len(i) == 5:#港股及香港ETF
                if 92959 < int(time.strftime("%H%M%S")) < 160959:#如果在交易时间内，取close列第二行
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                 asset='X', adj = 'qfq').close[1]
                else:
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                 asset='X', adj = 'qfq').close[0]
            else:
                '商品期货由于各品种夜盘时间不同，判断商品是否在交易时间内不严谨，可后续细化'
                '东方财富的期货收盘价显示日期有误，例如其显示20171204的OCHL实际为20171205的'
                if 205959 < int(time.strftime("%H%M%S")) < 235959 or 0 < int(time.strftime("%H%M%S")) < 23000 \
                   or 85959 < int(time.strftime("%H%M%S")) < 145959:
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                 asset='X', adj = 'qfq').close[1]
                else:
                    ClosePrice[i] = ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,
                                 asset='X', adj = 'qfq').close[0]
    return ClosePrice
    
#PreClose = [ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today, asset='E', adj = 'qfq').close[0]
#            if i.isdigit() and len(i) == 6 else 
#            ts.bar(i, conn=cons, freq='D', start_date=TenDaysAgo, end_date=Today,asset='X', adj = 'qfq').close[0]
#            for i in TsSymbol.tolist()] #注意郑商所品种格式为fg1805或FG1805,FG805会出错

PreClose = Series(PreClose(TsSymbol).values())
Quotes = df({'TsSymbol': TsSymbol, 'PreClose': PreClose.map(format3)}, columns = ['TsSymbol', 'PreClose'])
#创建DataFrame时如果不指定columns参数的顺序，将默认按首字母顺序排序

def TsTickMonitor(L):
    '''
    如函数报错:'NoneType' object has no attribute 'iat'
    请检查个别品种是否不在交易时间，如夜盘时间无夜盘交易的商品期货
    '''
    TickPrice = OrderedDict()
    TickTime = OrderedDict()
    for i in L:
        if i.isdigit():
            if len(i) == 6:
                if i.startswith('1') or i.startswith('5'):#沪深场内基金
                    TickPrice[i] = ts.tick(i, conn=cons, date=Today, asset='E').iloc[-1,1]/10.0#倒数第一行第三列元素
                    TickTime[i] = ts.tick(i, conn=cons, date=Today, asset='E').iloc[-1,0]#timestamp type
                else:#沪深股票
                    TickPrice[i] = ts.tick(i, conn=cons, date=Today, asset='E').iloc[-1,1]
                    TickTime[i] = ts.tick(i, conn=cons, date=Today, asset='E').iloc[-1,0]
            if len(i) == 5 and i.startswith('0'):
                try:#港股ETF有6列，港股有4列，先try港股ETF
                    TickPrice[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,5]*0 + \
                                   ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,3]/1000.0
                    TickTime[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,0]
                except:#港股
                    TickPrice[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,2]/1000.0
                    TickTime[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,0]
        else:#字母+4位数字，国内商品期货
            TickPrice[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,2]/1000.0
            TickTime[i] = ts.tick(i, conn=cons, date=Today, asset='X').iloc[-1,0]
    return TickPrice, TickTime
     
Quotes['TickPrice'] = Series(TsTickMonitor(Quotes.TsSymbol)[0].values()).map(format3)
Quotes['TickTime'] = Series(TsTickMonitor(Quotes.TsSymbol)[1].values())    
Quotes['DiffRange(%)'] = ((Quotes['TickPrice'] / Quotes['PreClose'] - 1) * 100).map(format3)
print Quotes
Quotes.to_csv('Quotes.csv')

#test1 = ts.tick('00700', conn=cons, date=Today, asset='X').iat[-1,2]/1000
#test2 = ts.tick('00700', conn=cons, date=Today, asset='X').iloc[-1,2]/1000
#test3 = ts.tick('00700', conn=cons, date=Today, asset='X').tail(1)['price']/1000          
#if __name__=='__main__':
#    from timeit import Timer
#    t1=Timer("test1","from __main__ import test1")
#    t2=Timer("test2","from __main__ import test2")
#    t3=Timer("test3","from __main__ import test3")
#    print t1.timeit(1000000)
#    print t2.timeit(1000000)
#    print t3.timeit(1000000)
#    print t1.repeat(3,1000000)
#    print t2.repeat(3,1000000)
#    print t3.repeat(3,1000000)                
## 经测试，综合看iloc最快，tail(1)['列名']最慢，iat居中                    
                    

'''
1、找出上一个交易日
'''            