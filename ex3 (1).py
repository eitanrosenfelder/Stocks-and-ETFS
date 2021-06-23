#!/usr/bin/env python
# coding: utf-8

# # Exerice #3 in Financial DS - properties about etfs and selection of the best
# 

# In[2]:


#importing the libraries
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from openpyxl import Workbook
import requests
import re
from time import sleep
import random
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import yfinance as yf
import json
import csv


# In[11]:


#setting the needed options
path = "C:\\Users\\eitan\\Downloads\\chromedriver_win32_new\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(path, options=chrome_options)
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument('--no-sandbox')
chrome = webdriver.Chrome(path, options=chrome_options)


# In[12]:


#Collecting the properties for each etf of the list
def properties(etf):
    url = f'https://www.etf.com/{etf}#fit'
    path = "C:\\Users\\eitan\\Downloads\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(url)
    sleep(random.randint(40, 45))
    pe = driver.find_element_by_css_selector("#fundSharedHoldings+ .no-padding .rowText:nth-child(5) .pl0+ .pr0 .text-right").text
    sector_list = []
    rate = []
    sector = driver.find_elements_by_css_selector(".col-md-6 .column1 , .col-md-6 .pl0")
    for k in sector:
        g = k.text
        sector_list.append(g)  
    sector_list = sector_list[1:]
    sector_list, rate = sector_list[::2], sector_list[1::2]
    sector_df = pd.DataFrame(list(zip(sector_list, rate)),
                             columns =['sector', 'rate'])

    holdings = driver.find_element_by_css_selector('#fundSharedHoldings+ .no-padding .first+ .rowText .pl0+ .pr0 .text-right').text
    holdings = re.sub("[^0-9]", "",  holdings)
    holdings = int(holdings)
    holdings = float(holdings)
    geo_list = []
    geo = driver.find_elements_by_css_selector(".top10Holdings+ .pl0 .col-xs-12 .pl0+ .pr0 , .top10Holdings+ .pl0 .col-xs-12 .pl0")
    for i in geo:
        c = i.text
        geo_list.append(c)  

    geo_list, rate = geo_list[::2], geo_list[1::2]
    geo_df = pd.DataFrame(list(zip(geo_list, rate)),
                             columns =['geography', 'rate'])
    driver.close()
    return pe, holdings, sector_df, geo_df

    


# In[3]:


#givimg the list of etfs
list_etfs = ["IJH","VBR","VBK","SCHA","IWO","IJJ","SPMD","XMLV","MDYV","SLY","VIOO","IVOO","SMMV","REGL","FNX","EZM","JKK","JHSC","IVOV","AVUV","SILJ","VTWG","PTMC","AVDV","JKL","RWK","SBIO","JKJ","MFMS","XSMO","OUSM","EWZS","SGDJ","XSVM","XMHQ"]
len(list_etfs)


# In[13]:


#generating lists in order to keep the data I collect from the site
def making_lists(lst):
    sector_list = []
    pe_list= []
    geo_list= []
    holding_list = []
    sec = 'sector_df_'
    geo = 'geo_df_'
    p = 'pe_'
    h  = 'holdings_'
    for key in list_etfs:
        s = str(sec+key)
        sector_list.append(s)
        ho = str(h+key)
        holding_list.append(ho)
        g= str(geo+key)
        geo_list.append(g)
        pe = str(p+key)
        pe_list.append(ho)
    return sector_list, holding_list, geo_list, pe_list 

sector_list, holding_list, geo_list, pe_list = making_lists(list_etfs)
sector_list


# In[14]:


#collecting the data for all the etfs and saving the pe and holdings so I don't need to run again
def calling(list_etfs, sector_list, holding_list, geo_list, pe_list): 
    geo_dfs = {}
    sector_dfs = {}
    for i in range(0,len(list_etfs)):
        pe_list[i], holding_list[i], sector_list[i], geo_list[i] = properties(list_etfs[i])
        key_ = str(list_etfs[i])
        geo_dfs[i] = {key_ : pd.DataFrame(geo_list[i])}
        sector_dfs[i] = {key_ : pd.DataFrame(sector_list[i])}
    pe_holdings_df = pd.DataFrame(list(zip(list_etfs, pe_list, holding_list)),
                             columns =['etf', 'average pe', 'holdings'])
    return pe_holdings_df, geo_dfs, sector_dfs

pe_holdings_df, geo_dfs, sector_dfs = calling(list_etfs, sector_list, holding_list, geo_list, pe_list)
pe_holdings_df.to_csv('pe_holdings_df')

#saving the data collected about the sectors and geography spread in a json file so I don't need to run again
class JSONEncoder(json.JSONEncoder):
    def default(self, sector_dfs):
        if hasattr(sector_dfs, 'to_json'):
            return sector_dfs.to_json(orient='records')
        return json.JSONEncoder.default(self, sector_dfs)
with open('sector.json', 'w') as fp:
    json.dump(sector_dfs, fp, cls=JSONEncoder)
with open('geography.json', 'w') as fp:
    json.dump(geo_dfs, fp, cls=JSONEncoder)
    
pe_holdings_df


# In[68]:


geo_dfs


# In[69]:


sector_dfs


# In[39]:


#calling the data again
f = open('sector.json',) 
data_sector = json.load(f)

g = open('geography.json',) 
data_geography = json.load(g)
data_geography


# In[6]:


#making a data frame for the results
    
#collecting the change data and finding the interest dates and periods with keeping the results in a data frame
m1,m3,m6,y1,y2,y5=[],[],[],[],[],[]
for i in range(0,len(list_etfs)):
    sleep(random.randint(3, 5))
    tick = str(list_etfs[i])
    #printing where I am
    print(tick) 

    y = yf.Ticker(tick)
    ydf = y.history(start="2007-01-01", end="2020-11-30", interval="1mo")
    ydf['Date'] = ydf.index
    
    m1.append(ydf['Close'].pct_change().shift(1).iloc[-1])
    m3.append(ydf['Close'].pct_change().shift(3).iloc[-1])
    m6.append(ydf['Close'].pct_change().shift(6).iloc[-1])
    y1.append(ydf['Close'].pct_change().shift(12).iloc[-1])
    y2.append(ydf['Close'].pct_change().shift(24).iloc[-1])
    y5.append(ydf['Close'].pct_change().shift(60).iloc[-1])
    
rate_growth_df = pd.DataFrame(list(zip(list_etfs, m1, m3, m6, y1, y2, y5)),
                             columns =['etf', "1 month change",  "3 month change", "6 month change", "1 year change", "2 year change", "5 year change"])
rate_growth_df.to_csv('rate_growth_df')
rate_growth_df


# In[71]:


rate_growth_df.nlargest(n=1, columns="1 month change")


# In[72]:


rate_growth_df.nlargest(n=1, columns="3 month change")


# In[73]:


rate_growth_df.nlargest(n=1, columns="6 month change")


# In[74]:


rate_growth_df.nlargest(n=1, columns="1 year change")


# In[75]:


rate_growth_df.nlargest(n=1, columns="2 year change")


# In[76]:


rate_growth_df.nlargest(n=1, columns="5 year change")


# In[4]:


rate_growth_df = pd.read_csv("rate_growth_df.csv")
rate_growth_df.nlargest(n=10, columns="6 month change change")


# In[23]:


rate_growth_df.nsmallest(n=10, columns="1 year change")


# Outlook for 2021:
# 
# I would suggest to invest in these three etfs:
# 
# 1. IVOV
# 2. VIOO
# 
# These two because they did very well in the past five years (#3,4 out of the list), with the past year not being that good, therefore I expect a recovery in the coming year. Furthermore they have a significant percentage of holdings in the financial sector that is expected to go up. 
# 
# 3. VBK
# 
# Did well (#9 out of the list) in the past five years and has a high percent of holdings in healthcare with some financials and a bit in the energy sector. It was a tough choice between JKK and VBK, I preferred VBK since the past year went worse,  therefore I expect they will have a more steap growth. JKK had a better year with decreasing gains, while VBK had a worse year but we can see recovery.
