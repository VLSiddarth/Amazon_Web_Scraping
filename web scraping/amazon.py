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

'''
website_URL = "https://www.amazon.in/"
browser = webdriver.Chrome()
browser.get(website_URL)

# Navigate to the product page
best_sellers_link = browser.find_element(By.LINK_TEXT, "Best Sellers")

# Alternatively, you can find the anchor tag by its attributes
best_sellers_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/?ref_=nav_cs_bestsellers"]')

# Perform actions with the anchor tag, such as clicking it
best_sellers_link.click()
time.sleep(1)


clothes_link = browser.find_element(By.LINK_TEXT, "Clothing & Accessories")
clothes_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/ref=zg_bs_nav_apparel_0"]')
clothes_link.click()
time.sleep(1)

def scrape_product_details(num_products):
    wait = WebDriverWait(browser, 10)  # Adjust the timeout as needed
    
    for i in range(0, num_products + 1):
        xpath = '//*[@id="p13n-asin-index-' + str(i) + '"]'
        
        try:
            # Wait for the clothes item to be clickable
            clothes_item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            clothes_item.click()
            
            time.sleep(1)  # Add a short delay for the page to load

            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract product details
            product_title_element = soup.find('span', {'id': 'productTitle'})
            product_name = product_title_element.text.strip() if product_title_element else "Product name not found"
            
            # Extract other product details similarly...
            product_subtitle_element = soup.find('span', {'id': 'productSubtitle'})
            product_subtitle = product_subtitle_element.text.strip() if product_subtitle_element else "Product subtitle not found"

            price_parent_element = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')
            symbol = "Rs."  # Example symbol if found
            if price_parent_element:
                # If the element is found, proceed to extract the price
                price_element = price_parent_element.find('span', class_='a-price-whole')
                price = price_element.text.strip() if price_element else "Price not found"
            else:
                # Handle case when element is not found
                price = "Not found"

            # Extract the discount percentage
            discount_parent_element = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')

            if discount_parent_element:
                discount_element = discount_parent_element.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')
                discount = discount_element.text.strip() if discount_element else "Discount not found"
            else:
                discount = "Discount not found"

            # Extract the MRP price
            mrp_parent_element = soup.find('div', class_='a-section a-spacing-small aok-align-center')

            if mrp_parent_element:
                mrp_element = mrp_parent_element.find('span', class_='a-offscreen')
                mrp_price = mrp_element.text.strip() if mrp_element else "MRP price not found"
                # Replace the currency symbol
                mrp_price = mrp_price.replace('₹', 'Rs.')
            else:
                mrp_price = "MRP price not found"

            # Find the parent element containing the author information
            author_parent_element = soup.find('div', id='bylineInfo_feature_div')

            # Check if the parent element exists and then find the author element within it
            if author_parent_element:
                author_element = author_parent_element.find('a', class_='a-link-normal')
                # Extract the author's name if the author element is found
                author_name = author_element.text.strip() if author_element else "Author Name Not Found"
            else:
                author_name = "Author Parent Element Not Found"

            # Rating of the Book
            # Find the parent element containing the average customer reviews
            reviews_parent_element = soup.find('div', id='averageCustomerReviews_feature_div')

            # Check if the parent element exists and then find the elements within it
            if reviews_parent_element:
                # Extract the average rating
                average_rating_element = reviews_parent_element.find('span', class_='a-size-base')
                Rating_of_5stars = average_rating_element.text.strip() if average_rating_element else "Rating not found"

                # Extract the number of ratings
                num_ratings_element = reviews_parent_element.find('span', id='acrCustomerReviewText')
                num_ratings = num_ratings_element.text.strip() if num_ratings_element else "Number of ratings not found"

                # Define the fields and data to be written
                fields = ['Product Title', 'Author Name', 'Product Price', 'Discount Percentage', 'Product MRP', 'Ratings of 5 stars', 'Number of Ratings']
                mydict = {'Product Title': f'{product_name} {product_subtitle}',
                        'Author Name': f'{author_name}',
                        'Product Price': f'{symbol}{price}',
                        'Discount Percentage': f'{discount}',
                        'Product MRP': f'{mrp_price}',
                        'Ratings of 5 stars': f'{Rating_of_5stars}',
                        'Number of Ratings': f'{num_ratings}'}

                # Name of CSV file
                filename = "test.csv"

                # Writing to CSV file
                with open(filename, 'a', newline='') as csvfile:
                    # Creating a CSV writer object
                    writer = csv.DictWriter(csvfile, fieldnames=fields)

                    # Check if the file is empty
                    if csvfile.tell() == 0:
                        writer.writeheader()  # Write the header if the file is empty

                    # Writing data row
                    writer.writerow(mydict)
                # Write product details to CSV
                
        except Exception as e:
            print(f"Error occurred while scraping product {i}: {e}")
            
        finally:
            browser.back()  # Go back to the previous page to scrape the next product

    browser.quit()

# Example usage:
num_products = 2
scrape_product_details(num_products)
'''
options = ["Baby Boys", "Baby Girls"]

for option in options:
    print(option)

                        'Star Rating': f'{star_rating}',
                    'Percentage': f'{percentage}'