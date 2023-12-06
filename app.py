import pandas as pd
import polars as pl
import seaborn as snl
import requests
from bs4 import BeautifulSoup
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


# Making a driver instance

Service = webdriver.ChromeService(r"C:\Users\jj_jo\chromedriver.exe")
driver = webdriver.Chrome(service = Service)


# Website urls of hotels

urls = [
    "https://www.booking.com/hotel/kr/toyoko-inn-seoul-gangnam.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0", 
    "https://www.booking.com/hotel/kr/toyoko-inn-seoul-yeongdeungpo.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/peyto-samseong.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/fairfield-by-marriott-seoul.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/ibis-seoul.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/staz-doksan.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/shilla-stay-guro.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/bestwestern-premier-gangnam.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/ena-suite-namdaemun.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0",
    "https://www.booking.com/hotel/kr/four-points-by-sheraton-seoul-namsan.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0"
]
    



# Storing all scraped data in a list that will be used to make a dataframe later

list_of_names = []
list_of_ratings = []
list_of_reviews = []
first_3_reviews = []
list_of_prices = []


# Function to loop over all 10 urls

def loop_urls(urls):
    
    for url in urls:
        driver.get(url)
        
        handle_pop_up(driver, (By.ID, "onetrust-accept-btn-handler"))

        hotel_names = driver.find_elements(By.XPATH, '//h2[@class = "d2fee87262 pp-header__title" ]')
        ratings = driver.find_elements(By.XPATH, '//div[@class = "a3b8729ab1 d86cee9b25"]')
        reviews = driver.find_elements(By.XPATH, '//div[@class = "a53cbfa6de b5726afd0b"]')
                  
        
        for title in hotel_names:
            list_of_names.append(title.text)
            
        for rating in ratings:
            list_of_ratings.append(rating.text)
            
        for review in reviews: 
            list_of_reviews.append(review.text)
            

   
            
# Collecting every 4th rating
            
list_of_ratings = list_of_ratings[::4]


order1 = []
order2 = []
order3 = []

# Selecting the first 3 reviews of each hotel

def review_data(reviews):
    for index, review in enumerate(reviews):
       if index % 10 < 3:
           first_3_reviews.append(review)
    

review_data(list_of_reviews)

# 
reviews_in_order = [order1, order2, order3]


# My dictionary that will be used to make a df

my_dict = {
            "Hotel name": list_of_names,
            "Rating": list_of_ratings,
            "Review 1": [],
            "Review 2": [],
            "Review 3": []
    
    
    }



# Each hotel has 3 reviews, for every 3 reviews append them to review 1, 2, 3

def assign_review(reviews):
    for index, review in enumerate(reviews):
        
        if index % 3 == 0:
                my_dict["Review 1"].append(review)
                
        elif index % 3 == 1:
                my_dict["Review 2"].append(review)
                
        elif index % 3 == 2:
                my_dict["Review 3"].append(review)
        
      

assign_review(first_3_reviews)            
        


# make df from my_dict

hotel_details_df = pd.DataFrame(my_dict)




# Price and Room data:
    
p_and_r_url ="https://www.booking.com/hotel/kr/toyoko-inn-seoul-gangnam.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0"

# Running driver

def price_room_driver(driver, url):
    driver.get(url)


price_room_driver(driver , p_and_r_url)


# Dismissing the popup

def handle_pop_up(driver , locator):
    pop_up = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    pop_up.click()

    
handle_pop_up(driver, (By.ID, "onetrust-accept-btn-handler"))

# find all tr tags based on data block id 

all_tr_tags = driver.find_elements(By.TAG_NAME, "tr")


# Storing all data block ids in a 

data_block_ids = []


# extract the data block id from tr tags

def extract_data_block_id(tr_tags):
    for tr_tag in tr_tags:
        tag_attribute = tr_tag.get_attribute("data-block-id")
        data_block_ids.append(tag_attribute)
        

extract_data_block_id(all_tr_tags)


# Go into the id list if id is the one I want, find td tag, loop over it and extract price and room type

def price_and_room(driver, ids):
    for wanted_id in ids:
        # if this is the id 
        
        if wanted_id == "372714601_195175598_1_1_0" or wanted_id == "372714603_195175598_0_1_0":
            # find all tds then loop over desired td
            tds = driver.find_elements(By.TAG_NAME, "td")
            
            store_room_data = []
            store_price_data = []
            current_room_type = []
            
            for td in tds:
                room_attribute = td.get_attribute("class")
                price_attribute = td.get_attribute("class")
                
                if room_attribute == "hprt-table-cell -first hprt-table-cell-roomtype droom_seperator":
                    current_room_type = td.find_element(By.CLASS_NAME, "hprt-roomtype-link").text.replace("\n", ", ")
                    store_room_data.append(current_room_type)
                    
                    
                elif price_attribute == "hp-price-left-align hprt-table-cell hprt-table-cell-price   droom_seperator":
                        current_price = td.find_element(By.CLASS_NAME, "prco-valign-middle-helper").text
                        store_price_data.append(current_price)
                        
            
            
    return store_room_data, store_price_data
    
            
  
# 
store_room_data, store_price_data = price_and_room(driver, data_block_ids )    


# Creating a dictionary using price and room data

price_and_room_dict = {"Room type": store_room_data, "Price": store_price_data}


# Creating df from dictionary

price_and_room_df = pd.DataFrame(price_and_room_dict)
price_and_room_df




    

# Tomorrow !!
# Implement titles, review,rating etc for this single url
# create df for that
# try to run 10 urls and see if it works
# END!



