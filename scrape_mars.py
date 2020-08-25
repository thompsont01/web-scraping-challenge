#imports
import pandas as pd
import os
import requests
import warnings
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
warnings.filterwarnings('ignore')

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #news
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    html = browser.html
    sp = bs(html, 'html.parser')
    article = sp.find('div',class_='list_text')
    news_title = article.find('div',class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text


    #images
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    sp = bs(html,'html.parser')
    img_url = sp.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'

    #facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    html = browser.html 
    data_table = pd.read_html(facts_url)

    df = data_table[0]
    df.columns = ["Information", "Statistics"]
    #h_table = df.to_html(table_id = 'html_tbl_css',justify = 'left',index = False)
    mars_facts = df.to_html(classes = 'table table-striped')

    #hemispheres
    hemisphere_image_url =[]

    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    html = browser.html
    sp = bs(html,'html.parser')

    r = sp.find('div',class_ = 'result-list')
    hemispheres = r.find_all('div',class_='item')
    for h in hemispheres:
        name = h.find('h3').text
        name.replace('Enhanced','')
        end = h.find('a')['href']
        new_link = "https://astrogeology.usgs.gov/" + end
        browser.visit(new_link)
        html = browser.html
        sp = bs(html, 'html.parser')
        d = sp.find('div',class_ = 'downloads')
        i_url = d.find('a')['href']
        hemisphere_image_url.append({'Name': name, 'URL': i_url})

    #dictionary
    data = {"News_Title": news_title, "News_Description":news_p, "Image_URL": featured_image_url,"Mars_Facts_Table":mars_facts,"Hemisphere_Image_URL":hemisphere_image_url}

    browser.quit()
    return data
#print(scrape())

