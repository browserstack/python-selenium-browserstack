# python-selenium-browserstack
Run python tests on browserstack using the SDK.

## Prerequisite
```
python3 should be installed
```

## Setup
* Clone the repo
```
git clone -b sdk https://github.com/browserstack/python-selenium-browserstack.git
``` 
* Install packages through requirements.txt
```
pip3 install -r requirements.txt
```

## Set BrowserStack Credentials
* Add your BrowserStack username and access key in the `browserstack.yml` config fle.
* You can also export them as environment variables, `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY`:

  #### For Linux/MacOS
    ```
    export BROWSERSTACK_USERNAME=<browserstack-username>
    export BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
    ```
  #### For Windows
    ```
    setx BROWSERSTACK_USERNAME=<browserstack-username>
    setx BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
    ```

## Running tests
* Run sample test:
  - To run the sample test across platforms defined in the `browserstack.yml` file, run:
    ```
    browserstack-sdk ./tests/test.py
    ``` 
* Run tests on locally hosted website:
  - To run the local test across platforms defined in the `browserstack.yml` file, run:
    ```
    browserstack-sdk ./tests/local-test.py
    ``` 
