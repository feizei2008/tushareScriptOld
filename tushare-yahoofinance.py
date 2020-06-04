# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:32:57 2016

@author: zack zhang
"""

#l = ['aa','Bs','B22','44','3188.HK']
#for i in l:
#    if i.endswith('HK'):
#        print i
#        pass
    
#for i in l:
#    if i.isdigit() is True:
#        print '是数字'
#    else:# i.isdigit() is False：
#        print '非数字'
import datetime as dt
import tushare as ts
import pandas_datareader.data as web

today  = repr(dt.date.today())
today_5 = str(dt.date.today() - dt.timedelta(days = 5))
k = ts.get_hist_data('000040',start=today_5,end=today).loc[ts.get_hist_data('000040').index[0],'close']
print k



USDCNY = web.get_quote_yahoo(['CNY=X'])['last']
#USDHKD = web.get_quote_yahoo('HKD=X')['last']
#print USDHKD
print USDCNY



