#!/usr/bin/env python
# coding: utf-8

# In[2]:


#imports 

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from random import randint
import pandas as pd
import time
import re

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options = options)
driver.set_page_load_timeout(25)


# In[3]:


class Shopee_scraper:
    
    def seller_products(self, seller_name):
        seller_url = '{}{}'.format('https://shopee.sg/', seller_name)
        delay = 20
        next_page = 0
        counter = 0
        product_links = []
        product_descriptions = []
        product_prices = []
        product_discounts = []
        product_sold_count = []
        while next_page == 0:
            page_url = '{}{}{}{}'.format(seller_url, '?page=', counter, '&sortBy=pop')
            driver.get(page_url)
            try:
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.shop-all-product-view')))
                for i in range(5):
                    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
                    time.sleep(1.5)
                search_items = driver.find_elements_by_css_selector('div.shop-search-result-view__item.col-xs-2-4')
                if len(search_items) == 0:
                    next_page = 1
                else:
                    for search_item in search_items:
                        product_link = search_item.find_element_by_css_selector('a').get_attribute('href')
                        product_description = (search_item.find_element_by_css_selector('div._1JAmkB').get_attribute("textContent")).encode('utf-8').strip() 
                        product_price = (search_item.find_element_by_class_name('_1w9jLI._37ge-4._2XtIUk').get_attribute("textContent")).encode('utf-8').strip()
                        try:
                            product_discount = (search_item.find_element_by_css_selector('div.shopee-badge.shopee-badge--fixed-width.shopee-badge--promotion').get_attribute("textContent")).encode('utf-8').strip()
                        except:
                            product_discount = ""
                        try:
                            product_sold = (search_item.find_element_by_css_selector('div._18SLBt').get_attribute("textContent").encode('utf-8').strip())
                        except:
                            product_sold = ""
                        product_links.append(product_link)
                        product_descriptions.append(product_description)
                        product_prices.append(product_price)
                        product_discounts.append(product_discount)
                        product_sold_count.append(product_sold)
                counter += 1
                time.sleep(randint(2, 7))
            except TimeoutException:
                next_page = 1
            continue
        data = pd.DataFrame({"Product Links": product_links, "Product Descriptions": product_descriptions, "Product Prices (Discounted -where applicable)": product_prices, "Product Discounts": product_discounts, "Product Sold Count": product_sold_count})
        export_csv = data.to_csv(seller_name, index = None, header = True)
        return data    
                        
       

    
        
        


# In[4]:


test = Shopee_scraper()
#test.seller_products("INPUT HERE")


