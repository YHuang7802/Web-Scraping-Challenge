#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies 
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#website to be scrapped
url = 'https://redplanetscience.com/'
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html,'html.parser')
# print(soup.prettify())


# In[5]:


# find the class for the the title and paragraph
article = soup.find('div', class_= 'list_text')
print(article)


# In[6]:


# latest news title
title = article.find('div', class_= 'content_title').text

title


# In[7]:


# latest news title's teaser body
paragraph = article.find('div', class_= 'article_teaser_body').text

paragraph


# In[8]:


#website to be scrapped
url2 = 'https://spaceimages-mars.com/'
browser.visit(url2)


# In[9]:


html2 = browser.html
soup2 = BeautifulSoup(html2, 'html.parser')

image = soup2.find('img', class_= 'headerimage fade-in')

# print image url
print(f'{url2}{image["src"]}')


# In[10]:


#website to be scrapped
url3= "https://galaxyfacts-mars.com/"


# In[11]:


#scrape table
table = pd.read_html(url3)

#convert into df
comp_table = table[0]

#change header
header = comp_table.iloc[0]

comp_table = comp_table[1:]

comp_table.columns = header

# print table
comp_table


# In[12]:


# #website to be scrapped
url3= "https://marshemispheres.com/"
browser.visit(url3)


# In[13]:


html3 = browser.html
soup3 = BeautifulSoup(html3, 'html.parser')


# In[14]:


# empty lists
links = []
image_url =[]
titles =[]

area = soup3.find_all('a', class_ ='itemLink')

for each in area:
    try:
        link = each.get('href')
        if link not in links:
            links.append(link)
        browser.visit(url3 + link)
        
        #scrape for image url
        html3 = browser.html
        soup3 = BeautifulSoup(html3, 'html.parser')
        downloads = soup3.find('div', class_= 'downloads')
        anchor = downloads.a
        href = anchor.get('href')
        
         # Scrape for titles
        title = soup3.find('div', class_ = 'cover')
        name = title.h2.text
        
        # If image link not in the list, append
        if url3 + href not in image_url:
            image_url.append(url3 + href)
            
         # If title not in the list, append
        if name not in titles:
            titles.append(name)
    except:
            pass

hemisphere_image_urls = [{"title": titles[0], "img_url": image_url[0]},
                         {"title": titles[1], "img_url": image_url[1]},
                         {"title": titles[2], "img_url": image_url[2]},
                         {"title": titles[3], "img_url": image_url[3]},]
     
hemisphere_image_urls


# In[ ]:





# In[ ]:




