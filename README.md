# python-selenium-browserstack

## Prerequisite
```
python3 and pip3 should be installed
```

## Steps to run test session

1. Install packages through requirements.txt
```
pip3 install -r requirements.txt
```
2. Update your credentials in .env file
```dotenv
BROWSERSTACK_USERNAME="BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY="BROWSERSTACK_ACCESS_KEY"
URL="https://hub.browserstack.com/wd/hub"
```
3. Change the capabilities if you wish:
(For single test session, Navigate to ./scripts/single.py)
```python
desired_cap = {
  ...
 'browserName': 'iPhone',
 'device': 'iPhone 11',
 'realMobile': 'true',
 'os_version': '14.0',
 'name': 'BStack-[Python] Sample Test', # test name
 'build': 'BStack Build Number 1' # CI/CD job or build name
 ...
}
```

2. Run tests
  a. For single
  ```
  python3 ./scripts/single.py
  ```
  a. For local
  With step 1 also add your browserstack access key to ./scripts/local.py
  ```
  python3 ./scripts/local.py
  ```
  c. For parallel
  ```
  python3 ./scripts/parallel.py
  ```