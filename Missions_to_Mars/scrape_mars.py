# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info ={}
    
    # ----------------------------------------------------#
    # Retrieve the Mar's news title and paragraph
    # Visit the following URL for Mar's news to be scraped
    # ----------------------------------------------------#
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # ----------------------------------------------------#
    # Get the latest news title and its corresponding paragraph 
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text
    # ----------------------------------------------------#
    # ----------------------------------------------------#
    # Scrape for the Mars featured Image
    url = 'https://spaceimages-mars.com'
    browser.visit(url) 

    # Use Splinter to Click Button with the tag button
    full_image_button = browser.find_by_tag("button")[1]
    full_image_button.click()

    # Parse HTML object with Beautiful Soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Find the tag and class that contains this specific image 
    feature_img_url_path = img_soup.find('img', class_='headerimage').get('src')
    
    # Use the base url to create an absolute url
    featured_image_url = url + feature_img_url_path
    
    # ----------------------------------------------------#
    # ----------------------------------------------------#
    # Get the Mar's facts 
    # ----------------------------------------------------#
    # Use 'read_html' to scrape the facts table into a dataframe
    df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    # Assign columns and set index of dataframe
    df.columns=['Mars Description', 'Value']
   
    # Convert dataframe into HTML format
    mars_df = df.to_html()
    # ----------------------------------------------------#
    # ----------------------------------------------------#
    # Visit Mars hemispheres 
    mars_hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all 4 items about mars hemispheres
    items = soup.find_all('div', class_='item')

    # The list for hemisphere urls 
    the_hemisphere_image_urls = []
    hemispheres_main_url = 'https://marshemispheres.com/'

    # Loop through the items
    for i in items: 
        # Get the title
        title = i.find('h3').text

        # We need to build the link to the full image website. We already have the
        # main url namely https://marshemispheres.com/ but need to build on this.
        # In other words get the "cerberus.html" part for the first of the four items.
        # This will be appended to the main url to build the full image website
        # https://marshemispheres.com/cerberus.html in the first item is an example.
        build_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Now visit the full image website 
        browser.visit(hemispheres_main_url + build_img_url)
    
        # HTML Object of individual hemisphere information website 
        build_img_html = browser.html

        # Parse HTML object with Beautiful Soup
        soup = BeautifulSoup( build_img_html, 'html.parser')
    
        # Get the full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append to create the list of dictionaries 
        the_hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # ----------------------------------------------------#
    
    # Mars Dictionary
    mars_info  = {
    "news_title": news_title,
    "news_p": news_p, 
    "featured_image_url": featured_image_url,  
    "mars_fact_table": str(mars_df),
    "the_hemisphere_image_urls": the_hemisphere_image_urls  
    }
 
    return mars_info
