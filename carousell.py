import misc
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def openWebDriver():
    # Load The Web Driver Options
    chromeOptions = loadWebDriverOptions()

    # Create a new Chrome browser instance
    driver = webdriver.Chrome(options=chromeOptions)

    # Navigate to a website
    driver.get(misc.CAROUSELL_BASE_FRONTEND_URL)

    # Return Web Driver
    return driver

def closeWebDriver(driver=webdriver.Chrome):
    # Close the Web Driver (Browser Windows)
    driver.close()
    return True

def loadWebDriverOptions():
    # Set up Chrome options
    chromeOptions = Options()

    # Set the custom User-Agent
    chromeOptions.add_argument(f'--user-agent={misc.HTTP_USER_AGENT}')

    # Return Chrome Options
    return chromeOptions

def loginAndSaveCookies():
    # Open The Web Driver
    driver = openWebDriver()

    # Wait Until User Success Login
    input('Press Enter When You Finished Login...')

    # Save Cookies
    pickle.dump(driver.get_cookies(), open(misc.CAROUSELL_COOKIES_FILE_NAME, 'wb'))
    print(f'Cookies Saved: {misc.CAROUSELL_COOKIES_FILE_NAME}')

    # Close the Web Driver
    closeWebDriver()

def loadCookies(driver=webdriver.Chrome):
    # Load Cookies From File
    cookies = pickle.load(open(misc.CAROUSELL_COOKIES_FILE_NAME, 'rb'))
    for cookie in cookies:
        # Add Cookies
        driver.add_cookie(cookie)
    
    # For Safe
    time.sleep(0.1)
    driver.refresh()

    print(f'Cookies Loaded: {misc.CAROUSELL_COOKIES_FILE_NAME}')

    return True





driver = openWebDriver()

# Load Cookies
loadCookies(driver)

# Sell Button
# //*[@id="root"]/div/div/div/div/button

print(driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/button'))

input('Press Enter To Kill The Browser...')

# Close the browser
closeWebDriver(driver)