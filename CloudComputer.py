
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "livxy_mL6uPR"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "AenPNd1wTQEtBA233FVk"

CONFIG = json.load(open("config.json"))

URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "browserstack-build-1"
capabilities = [
    {
        "browserName": "Chrome",
        "browserVersion": "103.0",
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "BStack Python sample parallel", # test name
        "buildName": BUILD_NAME,  # Your tests will be organized within this build
    },
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
    switcher = {
        "chrome": ChromeOptions(),
        # "firefox": FirefoxOptions(),
        # "edge": EdgeOptions(),
        # "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())

def run_session(cap):
    username = "livxy_mL6uPR"
    access = "AenPNd1wTQEtBA233FVk"
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": username,
        "accessKey": access,
        "idleTimeout": 300,
    }
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
    try:
        run_session_2(driver)
    except Exception as err:
        message = f"Exception: {str(err.__class__)}{str(err.msg)}"
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
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
    # Open Facebook using bstack driver
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("Facebook"))
    # Send keys and enter email
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys('da')
    # Say success if the email is entered
    time.sleep(300)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Email has been successfully entered!"}}')
    
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')


for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()