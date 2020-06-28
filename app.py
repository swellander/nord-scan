import re
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sms import send
# from dotenv import load_dotenv
from loading_spinner import Spinner

# Load environment variables
# load_dotenv()

# Constants
# target = os.getenv('TARGET')
target = "nord"
url = os.getenv('MONITORED_URL')
url = "https://seattle.craigslist.org/search/sss?query=nord&sort=rel&srchType=T&bundleDuplicates=1&searchNearby=2&nearbyArea=217&nearbyArea=233&nearbyArea=350&nearbyArea=322&nearbyArea=94&nearbyArea=324&nearbyArea=654&nearbyArea=655&nearbyArea=466&nearbyArea=321&nearbyArea=9&nearbyArea=368&nearbyArea=459&nearbyArea=232&nearbyArea=461&nearbyArea=95&nearbyArea=325&nearbyArea=246"
list_selector = os.getenv('LIST_SELECTOR')
item_selector = os.getenv('ITEM_SELECTOR')
success_msg = os.getenv('SUCCESS_MSG', f'Success! Your target was found at {url}')


def item_is_in_list(list_items=[]):
    return any(target.lower() in item.text.lower() for item in list_items)


def get_chrome_driver():
    chrome_bin = os.getenv('GOOGLE_CHROME_SHIM')
    executable_path = str(os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver'))
    chrome_options = Options()
    chrome_options.binary_location = chrome_bin
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--remote-debugging-port=9222')
    return webdriver.Chrome(
        executable_path=executable_path, options=chrome_options
    )


def run_scan():
    print(f'Scanning for target: {target}')
    print(f'at url: {url}')
    print('====================================================')

    driver = get_chrome_driver()
    driver.implicitly_wait(3000)
    driver.get(url)

    num_jobs = 0

    # Wait for page to load
    print('Waiting for page to load')
    with Spiner():
        time.sleep(10)
    print('Page loaded')

    print('Scanning')
    first_page = BeautifulSoup(driver.page_source, features="html.parser")
    import pdb; pdb.set_trace()

    # If searching for item within a list
    if list_selector:
        list_items = first_page.find_all(list_selector)
        if item_is_in_list(list_items):
            print('Item found!')
            send(success_msg)
            print(f'Text notification sent to {os.getenv("TO_NUMBER")}')
        else:
            print(f'Scanned {len(list_items)} items. Item not found :(')
        
    else:
        raise Exception('Must supply a value for LIST_SELECTOR')

run_scan()