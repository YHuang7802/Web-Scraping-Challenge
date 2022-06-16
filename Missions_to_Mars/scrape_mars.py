#!/usr/bin/env python
# coding: utf-8
# import dependencies 
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #scraping for latest title and paragraph
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # find the class for the the title and paragraph
    article = soup.find('div', class_= 'list_text')
   
    # latest news title
    news_title = article.find('div', class_= 'content_title').text

    # latest news title's teaser body
    news_para = article.find('div', class_= 'article_teaser_body').text



    #scraping for featured image
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    image = soup2.find('img', class_= 'headerimage fade-in')

    featured_image_url = url2 + image['src']



    #scraping for mars facts
    url3= "https://galaxyfacts-mars.com/"

    #scrape table
    table = pd.read_html(url3)

    #convert into df
    comp_table = table[0]

    #change header
    header = comp_table.iloc[0]

    comp_table = comp_table[1:]

    comp_table.columns = header

    comp_table_index = comp_table.set_index("Mars - Earth Comparison")


    # print table
    html_table = comp_table_index.to_html()




    # scraping for hemisphere
    url3= "https://marshemispheres.com/"
    browser.visit(url3)


    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

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
        
   #store data in a dictionary
    mars_data = { 
    "News_Title": news_title,
    "News_Paragraph": news_para,
    "Featured_Image":featured_image_url,
    "Facts": html_table,
    "Hemisphere":hemisphere_image_urls

   }
   # Quit the browser
    browser.quit()

    # Return our dictionary
    return mars_data

print("code is working!!")