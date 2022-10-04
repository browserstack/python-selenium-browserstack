from dotenv import load_dotenv
import os
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "BROWSERSTACK_ACCESS_KEY"
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"

bstack_options = {
    "os" : "OS X",
    "osVersion" : "Monterey",
    "buildName" : "browserstack-build-1",
    "sessionName" : "BStack single python",
    "userName": BROWSERSTACK_USERNAME,
    "accessKey": BROWSERSTACK_ACCESS_KEY
}
bstack_options["source"] = "python:sample-main:v1.0"
options = ChromeOptions()
options.set_capability('bstack:options', bstack_options)
driver = webdriver.Remote(
    command_executor=URL,
    options=options)
try:
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
    ## Get text of product in cart
    item_in_cart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text
    # Verify whether the product (iPhone 12) is added to cart
    if item_on_page == item_in_cart:
        # Set the status of test as 'passed' if item is added to cart
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')
    else:
        # Set the status of test as 'failed' if item is not added to cart
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "iPhone 12 not added to the cart!"}}')
except NoSuchElementException as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
# Stop the driver
driver.quit()
