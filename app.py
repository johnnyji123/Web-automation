import pandas as pd
import requests
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        hotel_names = driver.find_elements(By.XPATH, '//h2[@class = "d2fee87262 pp-header__title" ]')
        ratings = driver.find_elements(By.XPATH, '//div[@class = "a3b8729ab1 d86cee9b25"]')
        reviews = driver.find_elements(By.XPATH, '//div[@class = "a53cbfa6de b5726afd0b"]')
                  
        
        for title in hotel_names:
            list_of_names.append(title.text)
            
        for rating in ratings:
            list_of_ratings.append(rating.text)
            
        for review in reviews: 
            list_of_reviews.append(review.text)
            


loop_urls(urls)   
            

# Collecting every 4th rating
list_of_ratings = list_of_ratings[::4]


# Selecting the first 3 reviews of each hotel
def review_data(reviews):
    for index, review in enumerate(reviews):
       if index % 10 < 3:
           first_3_reviews.append(review)
    

review_data(list_of_reviews)


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
hotel_details_df


