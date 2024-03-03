import misc
import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

def sellProduct(productData):
    id = productData['id']
    title = productData['title']
    body = productData['body']
    tags = productData['tags']
    vendor = productData['vendor']
    price = productData['price']
    images = productData['images']
    
    pass




def test():
    driver = openWebDriver()

    # Load Cookies
    loadCookies(driver)

    # Find The Sell Button And Click
    xpath = '//*[@id="root"]/div/div/div/div/button'
    button = driver.find_element(By.XPATH, xpath)
    if button:
        # Click Sell Button
        button.click()
    else:
        print(f'{xpath} Not Found.')
        exit(-1)

    # Wait until the page finishes loading
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.ID, 'main')))
    time.sleep(0.1)
    # Find The Select Photos And Click
    xpath = '//*[@id="main"]/div/div[1]/label/input'
    driver.find_element(By.XPATH, xpath).send_keys(os.path.join(os.getcwd(), 'images/2009824297029.sassy-fascination-water-works-stem-bathtime-sassy-231616.jpg'))

    input('')

    if button:
        # Click Upload Button
        button.click()
    else:
        print(f'{xpath} Not Found.')
        exit(-1)

    input('Press Enter To Kill The Browser...')

    # Close the browser
    closeWebDriver(driver)