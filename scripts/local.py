from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from browserstack.local import Local
from selenium.common.exceptions import NoSuchElementException

# Creates an instance of Local
bs_local = Local()

# You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
bs_local_args = { "key": "ACCESS_KEY" }

# Starts the Local instance with the required arguments
bs_local.start(**bs_local_args)

# Check if BrowserStack local instance is running
print(bs_local.isRunning())

desired_cap = {
 'browserName': 'iPhone',
 'device': 'iPhone 11',
 'realMobile': 'true',
 'os_version': '14.0',
 'name': 'BStack-[Python] Sample Test', # test name
 'build': 'BStack Build Number 1', # CI/CD job or build name
 'browserstack.local': 'true'
}

driver = webdriver.Remote(
    command_executor='https://USER_NAME:ACCESS_KEY@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
try:
    driver.get("http://bs-local.com:45691/check")
    body_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body'))).text
    # Verify whether the product (iPhone 12) is added to cart
    if body_text == "Up and running":
        # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Local Test ran successfully"}}')
except NoSuchElementException:
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Local test setup failed"}}')
# Stop the driver
driver.quit() 