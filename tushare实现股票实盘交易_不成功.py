# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 16:59:28 2016

@author: zack zhang
"""
import pandas as pd
from pandas import DataFrame

#import tushare as ts
#ts.set_token('')
#print ts.get_token()
#fd = ts.Future()
#df = fd.Futu(exchangeCD='CCFX', field='secShortName,contractObject,minChgPriceNum,lastTradeDate,deliMethod')
#print df

import tushare as ts
ts.set_broker('htzq', user='', passwd='')
print ts.get_broker()
csc = ts.TraderAPI('htzq')#初始化交易接口
csc.login()#登录
baseinfo = csc.baseinfo()#获取账户基本信息
print baseinfo
print baseinfo['fundavl']#可用余额
print csc.position()#获取持仓列表

#csc.buy('000729', price=7.82, count=1000)#以7.82元买入1000股000729
#csc.buy('000729', price=7.82, amount=50000)#以7.82元买入000729股票5万元
#
#csc.sell('000729', price=8.82, count=100)#以8.82元卖出100股000729
#csc.sell('000729', price=8.82, amount=10000)#以8.82元卖出000729股票1万元
#
#csc.entrust_list()#获取委托列表。通过获取委托单列表的数据，才能进行撤单操作，部分数据会作为参数传递给撤单函数。
#csc.cancel(ordersno='262138,265447',orderdate='20160930,20160930')#撤单
#
#csc.deal_list(begin=20160920,end=20160929)#获取成交列表
#
#ts.get_realtime_quotes('000581')#单个股票实时行情监控
#ts.get_realtime_quotes(['600848','000980','000981'])#多个股票实时行情监控
#
## 原帖链接 http://mp.weixin.qq.com/s?__biz=MzAwOTgzMDk5Ng==&mid=2650833912&idx=1&sn=7c8f58dfc5e02d651134c0826102954e&mpshare=1&scene=2&srcid=10062ZyNlPyHEyBfRBpyKJ9p&from=timeline&isappinstalled=0#wechat_redirect
