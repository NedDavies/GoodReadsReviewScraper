#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time


# In[2]:
import argparse

parser = argparse.ArgumentParser(description='Supplying urls')

parser.add_argument("-url", "--goodreads_url", help="Determines the url used.", required = True)

args = parser.parse_args()

print(args.goodreads_url)

GoodReadsurl = r'https://www.goodreads.com/book/show/7303702-street-fighting-mathematics'
GoodReadsurl = args.goodreads_url


# In[3]:


#GoodReadsurl = r'https://www.goodreads.com/book/show/33237408-execution'
driver = webdriver.Chrome('chromedriver.exe')
driver.get(GoodReadsurl)

import requests
from bs4 import BeautifulSoup
import pandas as pd

goodreads = driver.page_source
soup=BeautifulSoup(goodreads) #prepare it for beautiful soup

reviewcontent = []
GRreviewer = []
StarRating = []
ReviewDate = []
GRreviews  = 0

goodreads = driver.page_source
soup=BeautifulSoup(goodreads) #prepare it for beautiful soup


time.sleep(8)


# In[4]:


try: 
    link = driver.find_element_by_xpath('//img[contains(@src, "//s.gr-assets.com/assets/gr/icons/icon_close-63734f04e7baaa77fbad796225e5724c.svg")]')
    link.click()
except: print('no pop up')


# In[5]:


for j in soup.select('span[id*="reviewTextCont"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:#pull out the information from speific elements using these attributes
        reviewcontent.append(j.get_text())
        GRreviews += 1
for k in soup.select('a[class="user"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:
        GRreviewer.append(k.get_text())
for m in soup.select('span[class="staticStars notranslate"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:
        StarRating.append(m.get_text())
for n in soup.select('a[class*="reviewDate createdAt right"]')[0:30]:
        ReviewDate.append(n.get_text())
            
pages = len(driver.find_elements_by_xpath('//a[contains(@onclick, "page=")]'))

print()

for i in range(2,(pages-1),1):
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    
    link = driver.find_element_by_xpath('//a[contains(@onclick, "page='+str(i)+'")]')# this is it!!!!! just change page number and trunk of url
    
    
    link.click()
    
    time.sleep(3)
    
    goodreads = driver.page_source
    soup=BeautifulSoup(goodreads) #prepare it for beautiful soup


# In[6]:


j=0
for j in soup.select('span[id*="reviewTextCont"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:#pull out the information from speific elements using these attributes
    reviewcontent.append(j.get_text())
    GRreviews += 1
print('Reviews  = '+str(len(soup.select('span[id*="reviewTextCont"]'))))
    
for k in soup.select('a[class="user"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:
    GRreviewer.append(k.get_text())
    #print(k.get_text)
print('Reviewers  = '+str(len(soup.select('a[class*="user"]'))))
for m in soup.select('span[class="staticStars notranslate"]')[0:len(soup.select('a[class*="reviewDate createdAt right"]'))]:
    StarRating.append(m.get_text())
    #print(m.get_text)
    #print('hello')
print('Ratings  = '+str(len(soup.select('span[class*=" staticStars notranslate"]'))))
for n in soup.select('a[class*="reviewDate createdAt right"]')[0:30]:
    #print(n.get_text)
    ReviewDate.append(n.get_text())
print('Dates  = '+str(len(soup.select('a[class*="reviewDate createdAt right"]'))))


driver.quit()

GRReviews=pd.DataFrame(columns=['Review']) #initialise dataframez
GRReviews['Review']=pd.Series(reviewcontent) #fill reviews column
GRReviews['rating']=pd.Series(StarRating) #fill ratings column
GRReviews['Reviewer'] = pd.Series(GRreviewer) #fill reviewers columns
GRReviews['Review Date'] = pd.Series(ReviewDate)#fill reviewers columns


# In[7]:

    GRReviews.to_csv('GRReviews.csv')


# In[ ]:




