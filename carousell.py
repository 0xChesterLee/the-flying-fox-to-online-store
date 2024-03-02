import misc
import sys
import os
import pickle
from selenium import webdriver


def loginAndSaveCookies():
    # Create a new Chrome browser instance
    driver = webdriver.Chrome()

    # Navigate to a website
    driver.get()

# Load cookies
cookies = pickle.load(open(misc.CAROUSELL_COOKIES_FILE_NAME, 'rb'))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

# Get the page title
title = driver.title
print('Page title:', title)

input('Press Enter to save cookies...')

# Save cookies
# pickle.dump(driver.get_cookies(), open(misc.CAROUSELL_COOKIES_FILE_NAME, 'wb'))

# Close the browser
driver.quit()