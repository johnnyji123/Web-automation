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






Service = webdriver.ChromeService(r"C:\Users\jj_jo\chromedriver.exe")
driver = webdriver.Chrome(service = Service)

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
    



list_of_names = []
list_of_ratings = []
list_of_reviews = []
first_3_reviews = []
list_of_prices = []

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
            
 
            
#loop_urls(urls)
            
list_of_ratings = list_of_ratings[::4]

# out of every 10, I need the first 3
    

def review_data(reviews):
    for index, review in enumerate(reviews):
        if index % 10 < 3:
            first_3_reviews.append(review)
    

review_data(list_of_reviews)


test ="https://www.booking.com/hotel/kr/toyoko-inn-seoul-gangnam.en-gb.html?checkin=2024-01-26&checkout=2024-01-27&group_adults=1&req_adults=1&no_rooms=1&group_children=0&req_children=0"

driver.get(test)

pop_up = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
pop_up.click()


