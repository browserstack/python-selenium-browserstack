from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from browserstack.local import Local
from selenium.common.exceptions import NoSuchElementException

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "BROWSERSTACK_ACCESS_KEY"
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"

# Creates an instance of Local
bs_local = Local()

# You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
bs_local_args = { "key": BROWSERSTACK_ACCESS_KEY }

# Starts the Local instance with the required arguments
bs_local.start(**bs_local_args)

# Check if BrowserStack local instance is running
print(bs_local.isRunning())

desired_cap = {
    'os': 'OS X',
    'os_version': 'Monterey',
    'browser': 'chrome',
    'browser_version': 'latest',
    'buildName': 'browserstack-build-1',
    'sessionName': 'BStack [python] Local',
    'browserstack.local': 'true',
    'browserstack.user': BROWSERSTACK_USERNAME,
    'browserstack.key': BROWSERSTACK_ACCESS_KEY,
}
desired_cap['browserstack.source'] = 'python:sample-selenium-3:v1.0'

driver = webdriver.Remote(
    command_executor=URL,
    desired_capabilities=desired_cap)
try:
    driver.get("http://bs-local.com:45691/check")
    body_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))).text
    # Verify whether the product (iPhone 12) is added to cart
    if body_text == "Up and running":
        # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Local Test ran successfully"}}')
except NoSuchElementException:
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Local test setup failed"}}')
except Exception:
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some exception occurred"}}')

# Stop the driver
driver.quit()

# stop local binary
bs_local.stop()
