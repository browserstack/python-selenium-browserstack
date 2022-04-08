<<<<<<< main
# python-selenium-browserstack

## Prerequisite
```
# If pip is not installed, you can install it using:
sudo easy_install pip

# If you prefer pip, then use the following command:
sudo pip install selenium

pip install browserstack-local
```

## Steps to run test session

1. Change the capabilities if you wish:
(For single test session, Navigate to ./scripts/single.py)
```python
desired_cap = {
 'browserName': 'iPhone',
 'device': 'iPhone 11',
 'realMobile': 'true',
 'os_version': '14.0',
 'name': 'BStack-[Python] Sample Test', # test name
 'build': 'BStack Build Number 1' # CI/CD job or build name
}

# Also use your Browserstack credentials
driver = webdriver.Remote(
    command_executor='https://USER_NAME:ACCESS_KEY@hub-cloud.browserstack.com/wd/hub',
    desired_capabilities=desired_cap)
```

2. Run tests
  a. For single
  ```
  python ./scripts/single.py
  ```
  a. For local
  With step 1 also add your browserstack access key to ./scripts/local.py
  ```python
  # You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
  bs_local_args = { "key": "ACCESS_KEY" }
  ```
  ```
  python ./scripts/local.py
  ```
  c. For parallel
  ```
  python ./scripts/parallel.py
  ```
=======

>>>>>>> main
