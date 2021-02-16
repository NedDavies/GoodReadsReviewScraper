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


GoodReadsurl = 'https://www.goodreads.com/book/show/7303702-street-fighting-mathematics'


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


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


# In[8]:


rating2stars = {'it was amazing':5, 'really liked it':4, 'liked it':3, 'it was ok':2, 'did not like it':1}
GRReviews['stars']= GRReviews['rating'].map(rating2stars)

# get star image
Review = Image.open('GRReview Elaine.png')

area = (266, 8, 286, 28)

Star = Review.crop(area)

Review.paste(Star, (114, 54)) 

Empty = Image.open('GRReview Elaine.png')
area = (342,8,362,28)
EmptyStar = Empty.crop(area)
EmptyStar

ratedit = Image.open('GRReview Elaine.png')
area = (208,10,264,25)
rateditimg = ratedit.crop(area)


rateditlen = rateditimg.size[1]
rateditwid = rateditimg.size[0]

img = Image.open("GRReview Blank.png")
imgsize = img.size


# In[9]:


GRReviews1 = GRReviews.dropna()

for i in range(len(GRReviews)):
    #open blank amazon review image
    img = Image.open("GRReview Blank.png")
    draw = ImageDraw.Draw(img) # rename draw command
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Lato-Light.ttf", 16) #instantiate amazon ember font
    # draw.text((x, y),"Sample Text",(r,g,b))
    
    Content = GRReviews1['Review'][i]
    if len(Content) > 90:
        for j in range(0,20,1):
            if Content[90-j] == " ":
                EOL1 = 90-j
                Line1 = Content[0:EOL1]
                break
        if len(Content) > 180:
            for k in range(0,20,1):
                if Content[180-k] == " ":
                    EOL2 = 180-k
                    Line2 = Content[EOL1+1:EOL2]
                    break
            if len(Content) > 270:
                for m in range(0,20,1):
                    if Content[270-m] == " ":
                        EOL3 = 270-m
                        Line3 = Content[EOL2+1:EOL3]+str("...")
                        break
            else: Line3 = Content[EOL2:len(Content)]
        else: Line2 = Content[EOL1+1:len(Content)]
    else: Line1 = Content[0:len(Content)]
        
    draw.text((85,28), Line1,(0,0,0),font=font)
    draw.text((85,75), Line2,(0,0,0),font=font)
    draw.text((85,102), Line3,(0,0,0),font=font)
    
    draw.text((85,15), GRReviews1['Reviewer'][i], (0, 102, 106), font=ImageFont.truetype("Lato-Regular.ttf",20))
    
    
    rating = int(GRReviews1['stars'][i])
    
    ReviewerName = GRReviews1['Reviewer'][i]
    font=ImageFont.truetype("Lato-Regular.ttf",20)
    RNwidth = font.getsize(ReviewerName)[0]
    RNlength = font.getsize(ReviewerName)[1]
    img.paste(rateditimg, (85+RNwidth+5, 20))
    #img.save("C:/Users/nedge/OneDrive/Documents/The Pigeonhole/Data Analysis/Testsave/GRRev"+str(i+1)+".png")
    
    for n in range(rating):
        img.paste(Star, (85+RNwidth+rateditwid+10+n*20, 15)) 
    for p in range(5-rating):
        img.paste(EmptyStar, (85+RNwidth+rateditwid+90-p*20, 15))
    
    font = ImageFont.truetype("Lato-Regular.ttf", 20)
    Datewidth = font.getsize(GRReviews1['Review Date'][i])[0]
    draw.text((imgsize[0]-(10 +Datewidth),15), GRReviews1['Review Date'][i],(178,178,178),font=font)
    display(img)


# In[ ]:




