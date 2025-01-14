from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

from flipcart import get_availability, get_rating, get_review_count


def get_title(soup):

    try:
      
        title = soup.find("span", attrs={"id":'productTitle'})
        
       
        title_value = title.text

        
        title_string =title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

if __name__ == '_main_':

   
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    
    URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"

    
    webpage = requests.get(URL, headers=HEADERS)

    
    soup = BeautifulSoup(webpage.content, "html.parser")

    
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = []
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
   
    
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
amazon_df