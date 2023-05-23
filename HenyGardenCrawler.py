from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import pandas as pd
import time
import uuid

chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()

# Selenium close immediately after being launched successfully => use this command to ignore this
options.add_experimental_option('detach', True)
options.add_argument("--incognito")

class HenyGardenCrawler:
    # Constructor
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.sleep_time = 3

        # List of selectors & xpaths
        self._product_url_selector = '.product-thumb a'
        self._product_title_selector = '.product-name h1'
        self._product_desc_selector = '.pdp-product-highlights ul li'
        self._product_category_selector = '.breadcrumb li:nth-child(2) span'

        # --------------- when there is not discounted price --------------- #
        self._product_regular_price_selector = '.price-block .special-price span'
        # when there is discounted price
        self._product_regular_price_deleted_selector = '.pdp-price_type_deleted'

        self._product_image = '.slick-slide.slick-active .realclick img'

        # --------------- List of product info --------------- #
        self.product_url = ''
        self.product_title = ''
        self.product_desc = ''
        self.product_category = ''
        self.product_regular_price = ''
        self.product_images = ''
        self.product_shop = '' # Not yet
        self.product_attribute = ''  # Not yet
    
    def get_url(self, url):
        self.driver.get(url)

    def quit_url(self):
        self.driver.quit()

    def crawl_product_urls(self):
        product_urls = self.driver.find_elements(
            By.CSS_SELECTOR, self._product_url_selector)
        product_urls = [url.get_attribute('href') for url in product_urls]

        return product_urls
    
    def wait_until_the_whole_page_loaded(self):
        while True:
            elements = self.driver.find_elements(By.XPATH, "//html")
            loaded = all(element.is_displayed() for element in elements)
            if loaded:
                break
    
    def get_product_title(self):
        product_title = self.driver.find_element(By.CSS_SELECTOR, self._product_title_selector)
        self.product_title = product_title.text
    
    def get_product_category(self):
        product_category = self.driver.find_element(By.CSS_SELECTOR, self._product_category_selector)
        result = product_category.text
        if "HENY GARDEN" in result:
            result = result.replace("HENY GARDEN", "")
        self.product_category = result

    def get_product_regular_price(self):
        product_regular_price = self.driver.find_element(By.CSS_SELECTOR, self._product_regular_price_selector)
        raw_price = product_regular_price.text
        raw_price = raw_price.replace('₫', '')
        raw_price = raw_price.strip()
        raw_price = raw_price.replace(',', '')
        self.product_regular_price = raw_price

    def get_product_images(self):
        product_images = self.driver.find_elements(
            By.CSS_SELECTOR, self._product_image)
        product_images = [image.get_attribute(
            'src') for image in product_images]
        
        images_txt = ''

        for product_image in product_images:
            image_txt = str(product_image)
            images_txt += image_txt + "$"

        self.product_images = images_txt

    def generate_item_id(self):
        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)
        
        # Generate a UUID
        uuid_str = str(uuid.uuid4())
        
        # Concatenate the timestamp and UUID to create a unique ID
        item_id = f"{timestamp}-{uuid_str}"
        
        return item_id
    
    def append_product_to_list(self, products):
        try:
            products.append({
                "id": self.generate_item_id(),
                "title": self.product_title,
                "desc": self.product_desc,
                "regular_price": self.product_regular_price,
                "external_url": '',
                "images": self.product_images,
                "category": self.product_category
            })
            print("Added product successfully")
        except:
            print('Added product failed')
    
# --------------- Store products to csv (store_products_to_csv) --------------- 
    def createCSV(self, data, path):
        try:
            # Convert list of dictionaries to pandas dataframe
            df = pd.DataFrame(data)

            # Save dataframe to CSV file
            df.to_csv(path, sep="@", index=False, encoding='utf-8-sig')
        
        except Exception as e:
            pass  

    