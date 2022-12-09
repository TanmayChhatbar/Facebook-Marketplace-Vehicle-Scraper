import json
import os
import time
from threading import Thread

import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv.load_dotenv()

# Below the 2 constants - BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY - are read from the environment variables. 
# (You can also hardcode them in the code.) os.environ.get is used for Heroku deployment, os.getenv is used for local testing.
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or os.getenv("BROWSERSTACK_USERNAME") 
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or os.getenv("BROWSERSTACK_ACCESS_KEY")

# CONFIG (constant) is read from the config.json file.
CONFIG = json.load(open("config.json"))

# URL (constant) is read from the environment variables. (You can also hardcode it in the code.)
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
# BUILD_NANME (constant) is read from the environment variables. (You can also hardcode it in the code.)
BUILD_NAME = "browserstack-build-1"

# capabilities (array of dictionaries) is used to define the browsers that will be used for testing.
capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "103.0",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "BStack Python sample parallel", # test name
        "buildName": BUILD_NAME,  # Your tests will be organized within this build
    },
    # Below are the other browsers that can be used for testing. Uncomment one or more of them to use them.
    # (uncomment the same lines in the get_browser_option function [see lines 62-65])
    #
    # {
    #     "browserName": "Firefox",
    #     "browserVersion": "102.0",
    #     "os": "Windows",
    #     "osVersion": "10",
    #     "sessionName": "BStack Python sample parallel",
    #     "buildName": BUILD_NAME,
    # },
    # {
    #     "browserName": "Safari",
    #     "browserVersion": "14.1",
    #     "os": "OS X",
    #     "osVersion": "Big Sur",
    #     "sessionName": "BStack Python sample parallel",
    #     "buildName": BUILD_NAME,
    # },
]


def get_browser_option(browser):
    """get_broswer_option returns the browser options for the browser passed as argument.

    Args:
        browser (string): The browser for which the options are needed.

    Returns:
        Options: The options for the browser passed as argument.
    """
    switcher = {
        "chrome": ChromeOptions(),
        # "firefox": FirefoxOptions(),
        # "edge": EdgeOptions(),
        # "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())

def run_session(cap):
    """run_session runs the test session for the browser passed as argument.

    Args:
        cap (dictionary): The browser for which the test session is to be run.
    """    
    global BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
    
    # bstack_options is a dictionary that contains the BrowserStack specific options.
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
        "idleTimeout": 300,
    }
    # The following lines add the BrowserStack specific options to the options for the browser.
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    if "deviceName" in cap:
        bstack_options['deviceName'] = cap["deviceName"]
    if "deviceOrientation" in cap:
        bstack_options["deviceOrientation"] = cap["deviceOrientation"]
    if cap['browserName'] in ['ios']:
        cap['browserName'] = 'safari'
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    if cap['browserName'].lower() == 'samsung':
        options.set_capability('browserName', 'samsung')
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
    # The following lines are used to run the  session.
    try:
        run_session_2(driver)
    except Exception as err:
        message = f"Exception: {str(err.__class__)}{str(err.msg)}"
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    # The commented lines below can be used to run the test session.
    # except NoSuchElementException as err:
    #     message = f"Exception: {str(err.__class__)}{str(err.msg)}"
    #     driver.execute_script(
    #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    # except Exception as err:
    #     message = f"Exception: {str(err.__class__)}{str(err.msg)}"
    #     driver.execute_script(
    #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    # Stop the driver
    driver.quit()


def run_session_1(driver):
    """run_session_1 runs the test session for the browser passed as argument.

    Args:
        driver (webdriver): The webdriver for the browser for which the test session is to be run.
    """    
    driver.get("https://bstackdemo.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("StackDemo"))
    # Get text of an product - iPhone 12
    item_on_page = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/p'))).text
    # Click the 'Add to cart' button if it is visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="1"]/div[4]'))).click()
    # Check if the Cart pane is visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "float-cart__content")))
    # Get text of product in cart
    item_in_cart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text
    # Verify whether the product (iPhone 12) is added to cart
    if item_on_page == item_in_cart:
        # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')

def run_session_2(driver: str):
    """run_session_2 runs the test session for the browser passed as argument.

    Args:
        driver (webdriver): The webdriver for the browser for which the test session is to be run.
    """    
    # Open Facebook using bstack driver
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("Facebook"))
    # Send keys and enter email
    email = CONFIG['email'] or os.environ.get('EMAIL') or input('Enter email/phone number for FaceBook: ')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(email)
    password = CONFIG['password'] or os.environ.get('PASSWORD') or input('Enter password for FaceBook: ')
    # Say success if the email is entered
    time.sleep(300)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Email has been successfully entered!"}}')
    
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')


for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()