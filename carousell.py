import misc
import time
import pickle
import emoji
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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

def listProduct(productData=dict):
    # Define Product Data
    id = productData['id']
    title = emoji.demojize(productData['title'])
    body = emoji.demojize(productData['body'])
    vendor = productData['vendor']
    tags = productData['tags']
    price = productData['price']
    images = productData['images']

    # Init Web Driver
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
        return False

    # Wait until the page finishes loading
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.ID, 'main')))
    time.sleep(3)

    # Collection Picker Step 1
    xpath = '//*[@id="main"]/div/div[2]/div[30]' #Everything Else
    button = driver.find_element(By.XPATH, xpath)
    if button:
        # Click
        button.click()
    else:
        print(f'{xpath} Not Found.')
        return False

    # Wait until the page finishes loading
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'ReactModalPortal-COLLECTION_PICKER')))
    time.sleep(1)

    # Collection Picker Step 2 (Other)
    cssSelector = '#ReactModalPortal-COLLECTION_PICKER > div > div > div > div > div.M_Mv'
    button = driver.find_element(By.CSS_SELECTOR, cssSelector)
    if button:
        # Click
        button.click()
    else:
        print(f'{cssSelector} Not Found.')
        return False
    
    # Wait until the page finishes loading
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.XPATH, 'main')))
    time.sleep(1)

    # Upload Images
    xpath = '//*[@id="main"]/div/div[1]/label/input'
    for image in productData['images']:
        driver.find_element(By.XPATH, xpath).send_keys(image)
        time.sleep(1)

    # Wait until the page finishes loading
    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.XPATH, 'FieldSetField-Container-field_title')))
    time.sleep(1)

    # Scroll down using the keyboard keys
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)  # Scroll down one page
    time.sleep(0.1)

    # Product Title with Tags
    xpath = '//*[@id="FieldSetField-Container-field_title"]/div/div/div/input'
    text = driver.find_element(By.XPATH, xpath)
    if text:
        # Fill in Product Title Text with Tags
        text.clear()
        text.send_keys(f'{title} {tags}')
        time.sleep(1)
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Scroll down using the keyboard keys
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)  # Scroll down one page
    time.sleep(0.1)

    # Product Price Button (For Sale)
    xpath = '//*[@id="FieldSetField-Container-field_is_free"]/div/div[2]/div/button[1]/span'
    button = driver.find_element(By.XPATH, xpath)
    if button:
        try:
            button.click()
            time.sleep(1)
        except Exception as e:
            pass
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Scroll down using the keyboard keys
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)  # Scroll down one page
    time.sleep(0.1)
    
    # Product Price
    xpath = '//*[@id="FieldSetField-Container-field_price"]/div[1]/div/div/input'
    text = driver.find_element(By.XPATH, xpath)
    if text:
        # Fill in Product Price
        text.clear()
        text.send_keys(price)
        time.sleep(1)
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Product Condition (New)
    xpath = '//*[@id="FieldSetField-Container-field_condition"]/div/div[2]/div/button[1]'
    button = driver.find_element(By.XPATH, xpath)
    if button:
        try:
            button.click()
            time.sleep(2)
            button.click()
        except Exception as e:
            print(e)
            pass
    else:
        print(f'{cssSelector} Not Found.')
        return False

    # Product Description
    xpath = '//*[@id="FieldSetField-Container-field_description"]/div/div/div[1]/textarea'
    text = driver.find_element(By.XPATH, xpath)
    if text:
        # Fill in Product Description Body with Tags
        text.clear()
        text.send_keys(f'{body}\n{tags}')
        time.sleep(1)
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Scroll down using the keyboard keys
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)  # Scroll down one page
    time.sleep(0.1)
    
    # Optional Details Show More Button
    xpath = '//*[@id="main"]/div/form/div[1]/div[5]/div/button'
    button = driver.find_element(By.XPATH, xpath)
    if button:
        button.click()
        time.sleep(2)
    else:
        print(f'{xpath} Not Found.')
        return False

    # Check Box (I have more than one of the same item)
    cssSelector = '#FieldSetField-Container-field_multi_quantities > label > svg'
    button = driver.find_element(By.CSS_SELECTOR, cssSelector)
    if button:
        time.sleep(1)
        button.click()
        time.sleep(1)
    else:
        print(f'{cssSelector} Not Found.')
        return False
    
    # Check Box (Mailing & Delivery)
    cssSelector = '#FieldSetField-Container-field_mailing > label > svg'
    button = driver.find_element(By.CSS_SELECTOR, cssSelector)
    if button:
        button.click()
        time.sleep(1)
    else:
        print(f'{cssSelector} Not Found.')
        return False
    
    # Mailing & Delivery Text Description
    xpath = '//*[@id="FieldSetField-Container-field_mailing_details"]/div/div/div[1]/textarea'
    text = driver.find_element(By.XPATH, xpath)
    if text:
        # Fill in Product Title Text
        text.clear()
        text.send_keys(misc.MAILING_AND_DELIVERY_DESCRIPTION)
        time.sleep(1)
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Scroll down using the keyboard keys
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)  # Scroll down one page
    time.sleep(0.1)

    # List Now!
    xpath = '//*[@id="main"]/div/form/div[2]/button'
    button = driver.find_element(By.XPATH, xpath)
    if button:
        button.click()
        time.sleep(1)
    else:
        print(f'{xpath} Not Found.')
        return False
    
    # Wait For List Upload
    time.sleep(10)
    print(f'Listed On Carousell: {title}')

    # input('Press Enter To Do Next...')

    # Close the browser
    closeWebDriver(driver)

    return True
