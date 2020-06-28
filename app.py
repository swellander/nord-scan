import re
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from sms import send
# from dotenv import load_dotenv
from loading_spinner import Spinner

# Load environment variables
# load_dotenv()

# Constants
# target = os.getenv('TARGET')
target = "nord"
url = "https://seattle.craigslist.org/search/sss?query=nord&sort=rel&srchType=T&postedToday=1&bundleDuplicates=1&searchNearby=2&nearbyArea=217&nearbyArea=233&nearbyArea=350&nearbyArea=94&nearbyArea=324&nearbyArea=654&nearbyArea=655&nearbyArea=466&nearbyArea=321&nearbyArea=9&nearbyArea=368&nearbyArea=459&nearbyArea=232&nearbyArea=461&nearbyArea=95&nearbyArea=325&nearbyArea=246"
list_selector = os.getenv('LIST_SELECTOR')
item_selector = os.getenv('ITEM_SELECTOR')
success_msg = os.getenv('SUCCESS_MSG', f'Success! Your target was found at {url}')


def item_is_in_list(list_items=[]):
    return any(target.lower() in item.text.lower() for item in list_items)


def get_gecko_driver():
    firefox_bin = os.getenv('GOOGLE_CHROME_SHIM', '/Applications/Firefox.app')
    executable_path = str(os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/geckodriver'))
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(
        executable_path=executable_path, options=options
    )


cache = {}

def run_scan():
    print(f'Scanning for target: {target}')
    print(f'at url: {url}')
    print('====================================================')

    driver = get_gecko_driver()
    driver.implicitly_wait(3000)
    driver.get(url)

    num_jobs = 0

    # Wait for page to load
    print('Waiting for page to load')
    # with Spinner():
    #     time.sleep(10)
    print('Page loaded')

    print('Scanning')
    first_page = BeautifulSoup(driver.page_source, features="html.parser")

    keyboards = first_page.findAll('li', {'class': 'result-row'})

    num_hits = len(keyboards)
    print(f'{num_hits} hits')

    for keyboard in keyboards:
        title = keyboard.find_all('a', {'class': 'result-title'})[0].text
        price = keyboard.find_all('span', {'class': 'result-price'})[0].text
        time_posted = keyboard.find_all('time', {'class': 'result-date'})[0].get('datetime')
        link = keyboard.find_all('a', {'class': 'result-title'})[0].get('href')
    
        try:
            location = keyboard.find_all('span', {'class': 'nearby'})[0].text
        except IndexError:
            location = keyboard.find_all('span', {'class': 'result-hood'})[0].text
    
        msg = f'{title}\n{price}\nNear {location}\nPosted {time_posted}\n{link}'

        if not cache.get(msg):
            cache[msg] = msg
            send(msg)



while True:
    try:
        run_scan()
        time.sleep(2) # 1 hour
    except:
        send('Something went wrong...')

