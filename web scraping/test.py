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
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import pandas
import csv


website_URL = "https://www.amazon.in/"
browser = webdriver.Chrome()
browser.get(website_URL)

time.sleep(7)

# Navigate to the product page
best_sellers_link = browser.find_element(By.LINK_TEXT, "Best Sellers")

# Alternatively, you can find the anchor tag by its attributes
best_sellers_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/?ref_=nav_cs_bestsellers"]')

# Perform actions with the anchor tag, such as clicking it
best_sellers_link.click()
time.sleep(1)

# Find the anchor tag with the text "Books"
clothes_link = browser.find_element(By.LINK_TEXT, "Clothing & Accessories")
clothes_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/ref=zg_bs_nav_apparel_0"]')
clothes_link.click()
time.sleep(1)

x=1 #item number

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

    

# Example usage:
num_products = x
scrape_product_details(num_products)
time.sleep(1)

# Find the next page link
next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
# Click on the next page link to navigate to the next page
next_page_link.click()
time.sleep(1)

num_products = x
scrape_product_details(num_products)
time.sleep(1)
        
baby_link = browser.find_element(By.LINK_TEXT, "Baby")
baby_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/1953148031/ref=zg_bs_nav_apparel_1"]')
baby_link.click()
time.sleep(1)

num_products = x
scrape_product_details(num_products)
time.sleep(1)

# Find the next page link
next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
# Click on the next page link to navigate to the next page
next_page_link.click()
time.sleep(1)

num_products = x
scrape_product_details(num_products)
time.sleep(1)

options = ["Baby Boys", "Baby Girls"]

for option in options:
    try:
        select_option = browser.find_element(By.LINK_TEXT, option)
        select_option.click()
        time.sleep(3)
                
        # Perform actions specific to each category, such as scraping data or navigating further
        num_products = x
        scrape_product_details(num_products)
        time.sleep(1)

        # Find the next page link
        next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
        # Click on the next page link to navigate to the next page
        next_page_link.click()
        time.sleep(1)

        num_products = x
        scrape_product_details(num_products)

        # Wait for the page to load (adjust the time as needed)
        time.sleep(3)

        # Based on the selected option, handle the corresponding categories
        if option == "Baby Boys":
            
            # Handle categories specific to Baby Boys'
            categories_baby_boys = ["Accessories","Bodysuits","Christening Wear","Clothing Sets","Dungarees","Ethnic Wear","Footies","Innerwear","Jeans","Leggings","Pants","Rompers","Shirts","Shorts","Sleepwear","Suits & Blazers","Swimwear","T-Shirts & Polos","Trackpants & Joggers","Winter Wear"]
            for category in categories_baby_boys:
                category_element = browser.find_element(By.LINK_TEXT, category)
                category_element.click()
                time.sleep(1)
                # Add your logic for handling each category
                # Perform actions specific to each category, such as scraping data or navigating further                
                if category == "Accessories":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                    c_b_b_a = ["Hats & Caps","Leg Warmers","Neckerchiefs","Socks","Sunglasses","Tights"]
                    for c_b_a in c_b_b_a :
                        c_b_a_element = browser.find_element(By.LINK_TEXT, c_b_a)
                        c_b_a_element.click()
                        time.sleep(1)

                        if c_b_a == "Hats & Caps" :

                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)

                        elif c_b_a == "Leg Warmers":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 2
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Neckerchiefs":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 5
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Socks":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)

                            c_s = ["Ankle Socks","Crew Socks","Knee-High Socks"]
                            for cs in c_s:
                                cs_element = browser.find_element(By.LINK_TEXT, cs)
                                cs_element.click()
                                time.sleep(1)

                                if cs == "Ankle Socks":
                                    num_products = x
                                    scrape_product_details(num_products)
                                    time.sleep(1)

                                    # Find the next page link
                                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                                    # Click on the next page link to navigate to the next page
                                    next_page_link.click()
                                    time.sleep(1)

                                    num_products = 14
                                    scrape_product_details(num_products)

                                elif cs == "Crew Socks":
                                    num_products = 13
                                    scrape_product_details(num_products)
                                    time.sleep(1)
                                
                                elif cs == "Knee-High Socks":
                                    num_products = 2
                                    scrape_product_details(num_products)
                                    time.sleep(1)

                                else:
                                    category_element = browser.find_element(By.LINK_TEXT, "Accessories")
                                    category_element.click()
                                    time.sleep(1)

                        elif c_b_a == "Sunglasses":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 8
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Tights":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 3
                            scrape_product_details(num_products)
                            time.sleep(1)

                        else:
                            select_option = browser.find_element(By.LINK_TEXT, "Baby Boys")
                            select_option.click()
                            time.sleep(3)

                elif category == "Bodysuits":
                    # Perform actions specific to each category, such as scraping data or navigating further
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                elif category == "Christening Wear" :
                    skip = browser.find_element(By.XPATH, '//*[@id="CardInstancekJBcZHeAeSvAYaQINnPPEg"]/div[2]/div[1]/h4/text()')
                    continue  # Skip processing for this category and move to the next one

                elif category == "Clothing Sets" or "Dungarees":
                        # Perform actions specific to each category, such as scraping data or navigating further
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                elif category == "Ethnic Wear":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                    c_e = ["Dhotis,Mundus & Lungis","Ethnic Jackets","Kurta Sets","Kurtas","Pyjamas","Sherwanis"]
                    for ce in c_e:
                        ce_element = browser.find_element(By.LINK_TEXT, ce)
                        ce_element.click()
                        time.sleep(1)

                        if ce == "Dhotis,Mundus & Lungis":
                            num_products = 10
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ce == "Ethnic Jackets":
                            num_products = 0
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ce == "Kurta Sets":
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)

                        elif ce == "Kurtas":
                            num_products = 2
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ce == "Pyjamas":
                            skip = browser.find_element(By.XPATH, '//*[@id="CardInstanceSwSozY61GZU75NKtipxxBQ"]/div[2]/div[1]/h4/text()')
                            continue  # Skip processing for this category and move to the next one

                        elif ce == "Sherwanis":
                            num_products = 6
                            scrape_product_details(num_products)
                            time.sleep(1)

                        else:
                            baby_link = browser.find_element(By.LINK_TEXT, "Baby")
                            baby_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/1953148031/ref=zg_bs_nav_apparel_1"]')
                            baby_link.click()
                            time.sleep(1)


        elif option == "Baby Girls":
            # Handle categories specific to Baby Girls
            categories_baby_girls = ["Accessories","Bodysuits","Christening Wear","Clothing Sets","Dresses","Ethnic Wear","Footies","Innerwear","Jeans","Leggings","Overalls","Pants","Rompers","Skirts & Shorts","Sleepwear","Swimwear","Tops, T-Shirts & Shirts","Trackpants & Joggers","Winter Wear"]
            for category in categories_baby_girls:
                category_element = browser.find_element(By.LINK_TEXT, category)
                category_element.click()
                # Add your logic for handling each category

                if category == "Accessories":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                    c_b_b_a = ["Hats & Caps","Headbands","Leg Warmers","Neckerchiefs","Socks","Sunglasses","Tights"]
                    for c_b_a in c_b_b_a :
                        c_b_a_element = browser.find_element(By.LINK_TEXT, c_b_a)
                        c_b_a_element.click()
                        time.sleep(1)

                        if c_b_a == "Hats & Caps" :

                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)

                        elif c_b_a == "Headbands":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)
                            browser.back()
                            time.sleep(1)
                            browser.back()
                            time.sleep(1)

                        elif c_b_a == "Leg Warmers":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 4
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Neckerchiefs":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 2
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Socks":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)

                            # Wait for the page to load (adjust the time as needed)
                            time.sleep(3)

                            c_s = ["Ankle Socks","Crew Socks","Knee-High Socks"]
                            for cs in c_s:
                                cs_element = browser.find_element(By.LINK_TEXT, cs)
                                cs_element.click()
                                time.sleep(1)

                                if cs == "Ankle Socks":
                                    num_products = 11
                                    scrape_product_details(num_products)
                                    time.sleep(1)

                                elif cs == "Crew Socks":
                                    skip = browser.find_element(By.XPATH, '//*[@id="CardInstanceOeIBQkoGX2DYvK7MbbEqTg"]/div[2]/div[1]/h4/text()')
                                    continue  # Skip processing for this category and move to the next one
                                
                                elif cs == "Knee-High Socks":
                                    num_products = 0
                                    scrape_product_details(num_products)
                                    time.sleep(1)

                                else:
                                    category_element = browser.find_element(By.LINK_TEXT, "Accessories")
                                    category_element.click()
                                    time.sleep(1)

                        elif c_b_a == "Sunglasses":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 3
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif c_b_a == "Tights":
                            # Perform actions specific to each category, such as scraping data or navigating further
                            num_products = 9
                            scrape_product_details(num_products)
                            time.sleep(1)

                        else:
                            select_option = browser.find_element(By.LINK_TEXT, "Baby Girls")
                            select_option.click()
                            time.sleep(3)

                elif category == "Bodysuits":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)

                    # Wait for the page to load (adjust the time as needed)
                    time.sleep(3)

                elif category == "Christening Wear":
                    num_products = 4
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Clothing Sets":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Dresses":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Ethnic Wear":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    c_e = ["Bottomwear","Kurtas & Kurtis","Lehenga Cholis"]
                    for ce in c_e:
                        ce_element = browser.find_element(By.LINK_TEXT, ce)
                        ce_element.click()
                        time.sleep(1)

                        if ce == "Bottomwear":
                            skip = browser.find_element(By.XPATH, '//*[@id="CardInstanceOx-v16GRmz6XUl_hDEbRIw"]/div[2]/div[1]/h4/text()')
                            continue  # Skip processing for this category and move to the next one

                        elif ce == "Kurtas & Kurtis":
                            num_products = 13
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ce == "Lehenga Cholis":
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = 4
                            scrape_product_details(num_products)
                            time.sleep(1)

                        else:
                            select_option = browser.find_element(By.LINK_TEXT, "Baby Girls")
                            select_option.click()
                            time.sleep(3)

                elif category == "Footies":
                    num_products = 5
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Innerwear":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    c_i = ["Bloomers","Sets","Training Pants","Vests"]
                    for ci in c_i:
                        ci_element = browser.find_element(By.LINK_TEXT, ci)
                        ci_element.click()
                        time.sleep(1)

                        if ci == "Bloomers":
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ci == "Sets":
                            num_products = 18
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ci == "Training Pants":
                            num_products = 25
                            scrape_product_details(num_products)
                            time.sleep(1)

                        elif ci == "Vests":
                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                            # Find the next page link
                            next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                            # Click on the next page link to navigate to the next page
                            next_page_link.click()
                            time.sleep(1)

                            num_products = x
                            scrape_product_details(num_products)
                            time.sleep(1)

                        else:
                            select_option = browser.find_element(By.LINK_TEXT, "Baby Girls")
                            select_option.click()
                            time.sleep(3)

                elif category == "Jeans":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Leggings":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Overalls":
                    num_products = 33
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Pants":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                elif category == "Rompers":
                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                    # Find the next page link
                    next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
                    # Click on the next page link to navigate to the next page
                    next_page_link.click()
                    time.sleep(1)

                    num_products = x
                    scrape_product_details(num_products)
                    time.sleep(1)

                





                    

                    




        
                    
    except Exception as e:
        print(f"Option {option} not available: {e}")


                
        
        
            
            

    

clothes_link = browser.find_element(By.LINK_TEXT, "Clothing & Accessories")
clothes_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/ref=zg_bs_nav_apparel_0"]')
clothes_link.click()
time.sleep(1)

boys_link = browser.find_element(By.LINK_TEXT, "Boys")
boys_link = browser.find_element(By.CSS_SELECTOR, 'a[href="/gp/bestsellers/apparel/1967851031/ref=zg_bs_nav_apparel_1"]')
boys_link.click()
time.sleep(1)

num_products = 2
scrape_product_details(num_products)
time.sleep(1)

# Find the next page link
next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
# Click on the next page link to navigate to the next page
next_page_link.click()
time.sleep(1)

num_products = 2
scrape_product_details(num_products)
time.sleep(1)

# Find all the categories within the current section
category_elements = browser.find_elements(By.XPATH, "//div[@class='categories']//a")

# Extract the category names from the elements
categories = [category.text for category in category_elements]

# Loop through each category and click on it
for category in categories:
    try:
        # Find the category element and click on it
        category_element = browser.find_element(By.LINK_TEXT, category)
        category_element.click()

        # Wait for the page to load (adjust the time as needed)
        time.sleep(3)

        num_products = 2
        scrape_product_details(num_products)
        time.sleep(1)

        next_page_link = browser.find_element(By.XPATH, '//li[@class="a-last"]/a')
        # Click on the next page link to navigate to the next page
        next_page_link.click()
        time.sleep(1)

        num_products = 2
        scrape_product_details(num_products)
        time.sleep(1)                
    
    except Exception as e:
        print(f"An error occurred while processing {category} in {option}: {e}")

browser.quit()   


