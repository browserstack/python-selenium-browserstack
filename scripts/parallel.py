from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread
from selenium.common.exceptions import NoSuchElementException

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "BROWSERSTACK_ACCESS_KEY"
URL = "https://" + BROWSERSTACK_USERNAME + ":" + BROWSERSTACK_ACCESS_KEY + "@hub.browserstack.com/wd/hub"

# This array 'caps' defines the capabilities browser, device and OS combinations where the test will run
caps = [
    {
        'os_version': '10',
        'os': 'Windows',
        'browser': 'firefox',
        'browser_version': 'latest',
        'name': 'BStack [python] parallel 1',  # test name
        'build': 'browserstack-build-1',
    },
    {
        'os_version': 'Big Sur',
        'os': 'OS X',
        'browser': 'chrome',
        'browser_version': 'latest',
        'name': 'BStack [python] parallel 2',
        'build': 'browserstack-build-1',
    },
    {
        'device': 'Samsung Galaxy S20',
        'os_browser': '11.0',
        'name': 'BStack [python] parallel 3',
        'build': 'browserstack-build-1',
    }
]

# run_session function adds a product in cart bstackdemo.com

def run_session(desired_cap):
    desired_cap['browserstack.source'] = 'python:sample-selenium-3:v1.0'
    driver = webdriver.Remote(
        command_executor=URL,
        desired_capabilities=desired_cap)
    try:
        driver.get("https://bstackdemo.com/")
        WebDriverWait(driver, 5).until(EC.title_contains("StackDemo"))

        # Get text of an product - iPhone 12
        item_on_page = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/p'))).text

        # Check if "Add to cart" button is present
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="1"]/div[4]'))).click()

        # Check if the Cart pane is visible
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "float-cart__content")))

        # Get text of product in cart
        item_in_cart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text

        # Verify whether the product (iPhone 12) is added to cart
        if item_on_page == item_in_cart:
            # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')
    except NoSuchElementException:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some elements failed to load"}}')
    except Exception:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some exception occurred"}}')

    # Stop the driver
    driver.quit()


# The Thread function takes run_session function and each set of capability from the caps array as an argument to run each session in parallel
for cap in caps:
    Thread(target=run_session, args=(cap,)).start()
