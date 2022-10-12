# python-selenium-browserstack

## Prerequisite
```
python3 and pip3 should be installed
```

## Steps to run test session

- Install packages through requirements.txt
```
pip3 install -r requirements.txt
```
- Update your credentials in .env file
```dotenv
BROWSERSTACK_USERNAME="BROWSERSTACK_USERNAME"
BROWSERSTACK_ACCESS_KEY="BROWSERSTACK_ACCESS_KEY"
URL="https://hub.browserstack.com/wd/hub"
```

- Run tests

  a. For single
  ```
  python3 ./scripts/single.py
  ```
  b. For local
  ```
  python3 ./scripts/local.py
  ```
  c. For parallel
  ```
  python3 ./scripts/parallel.py
  ```
