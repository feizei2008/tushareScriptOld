# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 16:21:23 2017

@author: zack zhang
"""

import os
import pandas as pd
import tushare as ts
import datetime
import time
from collections import OrderedDict
#from decimal import getcontext, Decimal
from threading import Timer
import json
import csv
#import sys
#sys.getdefaultencoding() #Return ASCII
#tickArray = np.array([1,2,3])
#print type(tickArray)

from colorama import  init, Fore, Back#, Style  
init(autoreset=True)  
class Colored(object):  
  
    #  前景色:红色  背景色:默认  
    def red(self, s):  
        return Fore.RED + s + Fore.RESET  
  
    #  前景色:绿色  背景色:默认  
    def green(self, s):  
        return Fore.GREEN + s + Fore.RESET  
  
    #  前景色:黄色  背景色:默认  
    def yellow(self, s):  
        return Fore.YELLOW + s + Fore.RESET  
  
    #  前景色:蓝色  背景色:默认  
    def blue(self, s):  
        return Fore.BLUE + s + Fore.RESET  
  
    #  前景色:洋红色  背景色:默认  
    def magenta(self, s):  
        return Fore.MAGENTA + s + Fore.RESET  
  
    #  前景色:青色  背景色:默认  
    def cyan(self, s):  
        return Fore.CYAN + s + Fore.RESET  
  
    #  前景色:白色  背景色:默认  
    def white(self, s):  
        return Fore.WHITE + s + Fore.RESET  
  
    #  前景色:黑色  背景色:默认  
    def black(self, s):  
        return Fore.BLACK  
  
    #  前景色:白色  背景色:绿色  
    def white_green(self, s):  
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET  
  
color = Colored()  
#print color.red('I am red!')  
#print color.green('I am gree!')  
#print color.yellow('I am yellow!')  
#print color.blue('I am blue!')  
#print color.magenta('I am magenta!')  
#print color.cyan('I am cyan!')  
#print color.white('I am white!')  
#print color.white_green('I am white green!')

cons = ts.get_apis()
Today = datetime.date.today().strftime("%Y-%m-%d")
TenDaysAgo = (datetime.date.today() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")

#df2 = ts.tick('000725', conn=cons, date=Today, asset='E')#.iat[-1,3]/1000 #, market='KH', retry_count = 3
#tickPriceArray = df2.price.as_matrix() #dataframe的Series转为ndarray

#df1 = ts.bar('000501', conn=cons, freq='D', asset='E', start_date=Today, end_date='')#, adj = 'qfq'#bar没用market参数也可以
#print df1
#print '000501'+'当前价日内百分位',round((df1.close[0]-df1.low[0])/(df1.high[0]-df1.low[0])*100.0,2)

path = os.path.abspath(os.path.dirname(__file__))
Symbols = pd.read_csv(path+'\cninfo.csv',low_memory=False)
Symbols = Symbols.applymap(lambda x: x.replace(',','') )
format1 = lambda x: x.replace('.SH','').replace('.SZ','')
TsSymbol = Symbols['Symbol'].map(format1)

stocklist = ts.get_stock_basics()
#stocklist.to_csv('stocklist.csv')
time.sleep(10)
stocklist2 = stocklist.copy()
#with open('stocklist.csv', 'rb') as f:
#    stocklist2 = csv.reader(f)
#    f.close
namedict = stocklist2.loc[TsSymbol.tolist(),'name'].to_dict()
    
def dump(self, content, encoding='utf-8'):  
        # 只支持json格式  
        # indent 表示缩进空格数  
        return json.dumps(content, encoding=encoding, ensure_ascii=False)#, indent=4
        
def PreClose(L):
    ClosePrice = OrderedDict()
    for i in L:
        ClosePrice[i] = ts.bar(i, conn=cons, freq='D', asset='E', start_date=Today, end_date='').close
    return ClosePrice

PreClose = PreClose(TsSymbol)
PreCloseCopy = PreClose.copy() # 这句添加于20190311，相关变动在第122行
               
def DayTradeMonitor():
    print color.magenta('__Code__Name___Swing_DfRng__Pct___')
    for i in TsSymbol:   
        Monitor = OrderedDict()
        MonitorList = []
        Kbar = ts.bar(i, conn=cons, freq='D', asset='E', start_date=Today, end_date='')
        Monitor['Code'] = Kbar.code[0]
        Monitor['Name'] = namedict[i]#.decode('gb2312')
        Monitor['Swing'] = round((Kbar.high/Kbar.low - 1)*100.0,1)
        Monitor['DifferRange'] = round((Kbar.close[0]/PreCloseCopy[i] - 1)*100.0,2)
        Monitor['Pct'] = round((Kbar.close[0]-Kbar.low[0])/(Kbar.high[0]-Kbar.low[0])*100.0,2)        
#        Monitor['CodeSwingPct'] = Monitor['Code'], Monitor['Swing'], Monitor['Pct']
        MonitorList.append(Monitor)        
        for Monitor in MonitorList:
#            print json.dumps(Monitor.values(), encoding='utf-8', ensure_ascii=False)#cmd下显示乱码
#            print [x.encode('gb18030') if isinstance(x,str) else x for x in Monitor.values()]
#            print Monitor.values()[0],Monitor.values()[1].decode("utf-8").encode("gbk"),Monitor.values()[2:]#ipython下将decode，encode去掉即可
            if Monitor['Pct'] > 80:
                print Monitor['Code'],Monitor['Name'].decode("utf-8").encode("gbk"),color.red(str(Monitor.values()[2:]))
            elif Monitor['Pct'] < 20:
                print Monitor['Code'],Monitor['Name'].decode("utf-8").encode("gbk"),color.green(str(Monitor.values()[2:]))
#                print map(lambda x: x.decode('utf-8',errors='replace'), str(Monitor.values()))
            else:
                print Monitor['Code'],Monitor['Name'].decode("utf-8").encode("gbk"),Monitor.values()[2:]
    t = Timer(6,DayTradeMonitor)
    t.start()
    
if __name__ == "__main__": 
    DayTradeMonitor()
        

'''
1、实现多线程
2、获取保存个股多日（含T日）1min bar求出的22分钟ATR值
3、对ATR值取MA10
4、当实时ATR值涨/跌破ATR值的MA10，认为日内趋势来临，开始跟踪止盈/止损操作
5、隔3秒获取个股日内tick price ndarray
6、每次都获取tick的max/min值并update之
7、若最新tick price低于历史记录max值=0.2%，认为可市价跟踪止盈，或追涨买日内行情启动的股票（？），发出提示
8、若最新tick price高于历史记录min值=0.2%，认为可市价抄底买入，
4、跟踪日内截止目前新高/低
'''

'''
1、用tick price array计算boll bands
2、现价超出上轨，启动跟踪止盈逻辑
3、现价跌破下轨，启动抄底买入逻辑
'''

'''
with open实现开盘前一次性读取股票名称表、昨收价格表并存入csv，后续只读不写
'''

