# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 14:30:39 2017

@author: zack zhang
"""
import tushare as ts
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

df1 = ts.new_cbonds(default = 0)#转债列表，dataframe
df2 = ts.new_cbonds(default = 1)
dfk = ts.bar('128016', conn=cons)#转债日K线，dataframe
dftick = ts.tick('128016', conn=cons, date = '20171206')#转债tick行情，dataframe
dfquotes = ts.quotes('128016', conn=cons)#转债实时切片行情，一行
print dfquotes

'''
1、搞清正股和转债的联动内在逻辑关系（下调转股价等）
2、设定实时行情信号提醒参数
3、技术上实现实时提醒（首选微信）
'''