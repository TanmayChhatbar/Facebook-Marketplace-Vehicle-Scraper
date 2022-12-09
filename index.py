# Create a web driver that will be used to access the web page
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

setup = json.load(open("setup.json"))

# Create a web driver that will be used to access the web page
driver = webdriver.Chrome(executable_path=setup['facebook']['WebDriver_Path'])
# Open the web page
driver.get("https://www.facebook.com/")
# Wait for the page to load
driver.implicitly_wait(10)
# Find the email field and enter the email address
email = driver.find_element(By.ID, "email")
email.send_keys(setup['facebook']['email'])
# Find the password field and enter the password
password = driver.find_element(By.ID, "pass")
password.send_keys(setup['facebook']['password'])
# Find the login button and click it
login = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")
login.click()
# Wait until the page has loaded 
driver.implicitly_wait(10)

# Open marketplace tab
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[1]/ul/li[4]/span/div/a").click()
# Wait until the page has loaded
driver.implicitly_wait(10)

