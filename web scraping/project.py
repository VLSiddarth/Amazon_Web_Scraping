# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import pandas
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#driver = r"C:\\webdrivers.exe".replace("\\", "/")
# # Set webdriver path here, it may vary
#browser = webdriver.Chrome(options={driver_path:driver_path})
website_URL = "https://www.amazon.in/"
browser = webdriver.Chrome()
browser.get(website_URL)
time.sleep(9)

# Prompt the user to input the search query
search_query = input("Enter your search query: ")

# Locate the search bar element
search_bar = browser.find_element(By.CSS_SELECTOR, 'input[type="text"]#twotabsearchtextbox')

# Clear the search bar in case it already contains some text
search_bar.clear()

# Type the user input into the search bar
search_bar.send_keys(search_query)

# Press Enter key to perform the search
search_bar.send_keys(Keys.ENTER)

# Wait for a few seconds to see the result
time.sleep(5)

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

a = soup.find_all('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
for i in a:
      # Extract product details
    product_title_element = soup.find('span', {'id': 'productTitle'})
    product_name = product_title_element.text.strip() if product_title_element else "Null"
    
    # Extract other product details similarly...
    product_subtitle_element = soup.find('span', {'id': 'productSubtitle'})
    product_subtitle = product_subtitle_element.text.strip() if product_subtitle_element else "Null"

    price_parent_element = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')
    symbol = "Rs."  # Example symbol if found
    if price_parent_element:
        # If the element is found, proceed to extract the price
        price_element = price_parent_element.find('span', class_='a-price-whole')
        price = price_element.text.strip() if price_element else "Null"
    else:
        # Handle case when element is not found
        price = "Null"

    # Extract the discount percentage
    discount_parent_element = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')

    if discount_parent_element:
        discount_element = discount_parent_element.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')
        discount = discount_element.text.strip() if discount_element else "Null"
    else:
        discount = "Null"
    
                        
    # Extract the MRP price
    mrp_parent_element = soup.find('div', class_='a-section a-spacing-small aok-align-center')

    if mrp_parent_element:
        mrp_element = mrp_parent_element.find('span', class_='a-offscreen')
        mrp_price = mrp_element.text.strip() if mrp_element else "Null"
        # Replace the currency symbol
        mrp_price = mrp_price.replace('₹', 'Rs.')
    else:
        mrp_price = "Null"

