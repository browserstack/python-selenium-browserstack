from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread

def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())

def run_session(browser, browser_version, platform_name, os, osVersion, buildName, sessionName, seleniumVersion):
    desired_cap = {
        "os" : os,
        "osVersion" : osVersion,
        "buildName" : buildName,
        "sessionName" : sessionName,
        "seleniumVersion" : seleniumVersion,
    }

    options = get_browser_option(browser.lower())
    options.browser_version = browser_version
    options.platform_name = platform_name
    options.set_capability('bstack:options', desired_cap)
    driver = webdriver.Remote(
        command_executor='https://YOUR_USER_NAME:YOUR_ACCESS_KEY@hub-cloud.browserstack.com/wd/hub',
        options=options)
    try:
        driver.get("https://bstackdemo.com/")
        WebDriverWait(driver, 10).until(EC.title_contains("StackDemo"))
        # Get text of an product - iPhone 12
        item_on_page =  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/p'))).text
        # Click the 'Add to cart' button if it is visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/div[4]'))).click()
        # Check if the Cart pane is visible
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, "float-cart__content")))
        ## Get text of product in cart
        item_in_cart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text
        # Verify whether the product (iPhone 12) is added to cart
        if item_on_page == item_in_cart:
            # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "iPhone 12 has been successfully added to the cart!"}}')
    except NoSuchElementException:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some elements failed to load"}}')
    # Stop the driver
    driver.quit() 

Thread(target=run_session, args=("chrome", "latest", "MAC", "OS X", "Sierra", "parallel-snippet-test", "python 1", "4.0.0")).start()
Thread(target=run_session, args=("firefox", "latest", "MAC", "OS X", "Sierra", "parallel-snippet-test", "python 2", "4.0.0")).start()
Thread(target=run_session, args=("edge", "latest", "MAC", "OS X", "Sierra", "parallel-snippet-test", "python 3", "4.0.0")).start()
