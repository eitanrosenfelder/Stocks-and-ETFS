#!/usr/bin/env python
# coding: utf-8

# # Finding the cheeepest ad smallest subset of ETF's

# In[402]:


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


# In[195]:


#setting the needed options
path = "C:\\Users\\eitan\\Downloads\\chromedriver_win32_new\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(path, options=chrome_options)
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument('--no-sandbox')
chrome = webdriver.Chrome(path, options=chrome_options)


# In[313]:


#logging in
url = f'https://www.etfrc.com/funds/stocklocator.php'
path = "C:\\Users\\eitan\\Downloads\\chromedriver_win32_new\\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(url)
user = ********
psd = *****
log = driver.find_element_by_class_name("pe-7s-unlock")
log.click()
sleep(random.randint(5, 7))
mail = driver.find_element_by_css_selector("#Email")
mail.send_keys(user)
password = driver.find_element_by_css_selector("#Password")
password.send_keys(psd)
sleep(random.randint(15, 17))
log_in = driver.find_element_by_xpath('/html/body/div[2]/section/div/div[3]/div/div/div[2]/form/button')
log_in.send_keys(Keys.RETURN)


# In[332]:


#making a data frame with etfs corresponding to the stock
def collection(stock):
    search = driver.find_element_by_xpath('//*[(@id = "stockTicker")]')
    search.send_keys(stock)
    enter = driver.find_element_by_css_selector("#locatorBtn")
    enter.send_keys(Keys.ENTER)
    sleep(random.randint(260, 265))
    how_many = driver.find_element_by_css_selector("#ETFTable_length .input-sm")
    how_many.send_keys("All")
    sleep(random.randint(33, 35))
    how_many.send_keys(Keys.ENTER)
    sleep(random.randint(300, 315))
    
    etf_list = []
    weight_list = []

    weight = driver.find_elements_by_css_selector("td:nth-child(3)")
    for i in weight:
        print(i.text)
        w = i.text
        w = w.replace("%","")
        w = w.replace(" ","")
        w = float(w)
        weight_list.append(w)
    etf = driver.find_elements_by_css_selector("td:nth-child(1)")
    for i in etf:
        etf_list.append(i.text)
    df = pd.DataFrame(list(zip(weight_list, etf_list)), 
                   columns =['weight', 'etf'])
    company = df[df.weight > 4]
    return company


# In[333]:


#calling the function
stock_list = ["MSFT", "NVDA", "AAPL", "FB", "AMZN", "GOOGL", "NFLX"]
for i in range(1,len(stock_list)):
    print(i)
    if i == 1:
        df_MSFT = collection(stock_list[i])
    if i == 2:
        df_NVDA = collection(stock_list[i])
    if i == 3:
        df_AAPL = collection(stock_list[i])
    if i == 4:
        df_FB = collection(stock_list[i])
    if i == 5:
        df_AMZN = collection(stock_list[i])
    if i == 6:
        df_GOOGL = collection(stock_list[i])
    if i == 7:
        df_NFLX = collection(stock_list[i])


# In[356]:


#the best etfs for microsoft
new_price=float(100)
chosen_etf = []
etf_list = df_MSFT["etf"].values.tolist()
for j in range(1,len(etf_list)):
    etf = etf_list[j]
    etf_price = driver.find_element_by_css_selector("#fundticker")
    etf_price.send_keys(etf)
    etf_price.send_keys(Keys.ENTER)
    sleep(random.randint(7, 10))
    price = driver.find_element_by_css_selector(".row:nth-child(1) tr:nth-child(7) td+ td").text
    print(price)
    price = price.replace("bp","")
    price = price.replace(" ","")
    if price.isnumeric() == True:
        print(price)
        price = float(price)
        if price <= new_price:
            if price > 0:
                new_price = price
                chosen_etf.append(etf)
    else: 
        continue
chosen_etf


# In[405]:


#results
best_etf = chosen_etf
price_msft = new_price
type(best_etf)


# In[361]:


#the best etfs for the companies
def best(df):
    new_price=float(100)
    chosen_etf = []
    etf_list = df["etf"].values.tolist()
    for j in range(1,len(etf_list)):
        etf = etf_list[j]
        etf_price = driver.find_element_by_css_selector("#fundticker")
        etf_price.send_keys(etf)
        etf_price.send_keys(Keys.ENTER)
        sleep(random.randint(17, 0))
        price = driver.find_element_by_css_selector(".row:nth-child(1) tr:nth-child(7) td+ td").text
        print(price)
        price = price.replace("bp","")
        price = price.replace(" ","")
        if price.isnumeric() == True:
            print(price)
            price = float(price)
            if price <= new_price:
                if price > 0:
                    new_price = price
                    chosen_etf.append(etf)
        else: 
            continue
    return new_price, chosen_etf


# In[ ]:


#calling the function
price_nvda,best_nvda = best(df_NVDA)
print('nv')
price_aapl,best_aapl = best(df_AAPL)
print('ap')
price_fb,best_fb = best(df_FB)
print('fb')
price_amzn,best_amzn = best(df_AMZN)
print('am')
price_amzn,best_googl = best(df_GOOGL)
print('g')
price_amzn,best_nflx = best(df_NFLX)
print('nx')


# In[398]:


#making a full list without duplicates
best_set = best_etf

def common(best_set,new_set):
    for value in new_set:
        if value in best_set:
            return best_set
    best_set = best_etf.append(new_set)
    return best_set
best_set = common(best_set,best_nflx)
best_set = common(best_set,best_googl)
best_set = common(best_set,best_amzn)
best_set = common(best_set,best_fb)
best_set = common(best_set,best_aapl)
best_set = common(best_set,best_nvda)
best_set


# In[399]:


#preparing the final selection of etfs
def split_two_parts(full_list, n):
    return n_list[:n], n_list[n:]
best_set = split_two_parts(best_set, len(best_etf))
def extracting_best(lst): 
    return [item[0] for item in lst] 
best_etfs = extracting_best(best_set)
best_etfs

