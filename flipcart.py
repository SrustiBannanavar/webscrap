from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"class":'B_NuCI'}).text.strip()
    except AttributeError:
        title = ""
    return title

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("div", attrs={'class':'_30jeq3 _16Jk6d'}).text.strip()
    except AttributeError:
        price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("div", attrs={'class':'_3LWZlK'}).text.strip()
    except AttributeError:
        rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'class':'_2_R_DZ'}).text.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'class':'_16FRp0'}).text.strip()
    except AttributeError:
        available = "Available"
    return available

if _name_ == '_main_':
    # Add your user agent
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.flipkart.com/search?q=playstation+4"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'_1fQZEK'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append("https://www.flipkart.com" + link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get(link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    flipkart_df = pd.DataFrame.from_dict(d)
    flipkart_df['title'].replace('', np.nan, inplace=True)
    flipkart_df = flipkart_df.dropna(subset=['title'])
    flipkart_df.to_csv("flipkart_data.csv", header=True, index=False)

flipkart_df