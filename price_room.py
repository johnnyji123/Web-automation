import pandas as pd
import requests
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Making driver instance 

Service = webdriver.ChromeService(r"C:\Users\jj_jo\chromedriver.exe")
driver = webdriver.Chrome(service = Service)


# Price and Room url
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
    
            
  

store_room_data, store_price_data = price_and_room(driver, data_block_ids )    


# Creating a dictionary using price and room data
price_and_room_dict = {"Room type": store_room_data, "Price": store_price_data}


# Creating df from dictionary
price_and_room_df = pd.DataFrame(price_and_room_dict)
price_and_room_df




    





