from dotenv import load_dotenv
import os
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

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "BROWSERSTACK_ACCESS_KEY"
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"

capabilities = [
  {
    "os": "OS X",
    "osVersion": "Monterey",
    "buildName" : "browserstack-build-1",
    "sessionName" : "BStack parallel python",
    "browserName": "chrome",
    "browserVersion": "latest"
  },
  {
    "os": "Windows",
    "osVersion": "11",
    "buildName" : "browserstack-build-1",
    "sessionName" : "BStack parallel python",
    "browserName": "firefox",
    "browserVersion": "latest"
  },
  {
    "osVersion": "10",
    "deviceName" : "Samsung Galaxy S20",
    "buildName" : "browserstack-build-1",
    "sessionName" : "BStack parallel python",
    "browserName": "chrome",
  },
]

def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())

def run_session(cap):
    bstack_options = {
        "osVersion" : cap["osVersion"],
        "buildName" : cap["buildName"],
        "sessionName" : cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
      bstack_options["os"] = cap["os"]
    bstack_options["source"] = "python:sample-main:v1.0"
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
      options.browser_version = cap["browserVersion"]
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
            # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')
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

for cap in capabilities:
  Thread(target=run_session, args=(cap,)).start()
