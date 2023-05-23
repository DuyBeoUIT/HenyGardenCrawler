from HenyGardenCrawler import HenyGardenCrawler
import tkinter as ttk
import time
from colorama import Fore, Style

# --------------- Golbal scopes --------------- #
products = []

#--------------- Loop to simulate work being done (Loading in terminal) --------------- #
start, end = 0, 100

print(Fore.YELLOW + 'Preparing to start...' + Style.RESET_ALL)

for i in range(end):
    time.sleep(0.05)  # Simulate some work being done
    start += 1
    progress = start / end
    bar_length = 50
    filled_length = int(round(bar_length * progress))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percentage = round(progress * 100, 2)

    # Print colored progress bar
    print(Fore.GREEN + f'\r[{bar}] {percentage}% ' + Style.RESET_ALL, end='', flush=True)

print(Fore.YELLOW + '\nProgram Start' + Style.RESET_ALL)

def main():
    root_url = "https://henygarden.com/collections/nen-thom-cao-cap"

    henygarden_crawler = HenyGardenCrawler()

    henygarden_crawler.get_url(root_url)

    time.sleep(henygarden_crawler.sleep_time)

    product_urls = henygarden_crawler.crawl_product_urls()

    i = 0
    for product_url in product_urls:
        henygarden_crawler.get_url(product_url)

        henygarden_crawler.wait_until_the_whole_page_loaded()

        henygarden_crawler.get_product_title()

        henygarden_crawler.get_product_category()

        henygarden_crawler.get_product_regular_price()

        henygarden_crawler.get_product_images()

        henygarden_crawler.append_product_to_list(products)

    henygarden_crawler.quit_url()

    #set name for file csv with current time
    current = time.localtime()
    path_csv = "import_data_" + str(current.tm_hour) + str(current.tm_min) + str(current.tm_sec) + '.csv'
    henygarden_crawler.createCSV(products, path_csv)

main()