# noneqa

noneqa is an automatef testing framework skeleton to test API and UI parts of test assignment from NinjaOne.
It is implemented in python and uses Selenium for web-UI, and requests for REST API.

## Requirements
1. python 3.10.x is installed and available in PATH as python3.10
2. venv in installed

## Compatibility and assumptions
The project has been tested on Windows 11 platform. Should be platform indepenedent, but was not tested on Linux of Mac OS.


## Installation
```bash
git clone https://github.com/mityaika/noneqa.git
cd noneqa
python3.10 -m venv venv
.\venv\Scripts\activate  # for Windows
# or for Linux/Mac OS source ./venv/bin/activate
pip install -r requirements.txt
```

## Run tests
Open config/default.config file and adjust your URLs for client and server apps.
```bash
python -m pytest --html=testresults/report.html
```

## Test results
Results are output to console and html report created in testresults folder.

## Features and architecture
1. The framwework has extensive configuration options where config option can be provided via command-line, config files, environment variables. Default configuration is in config/default.config file.
2. The framework separates API, UI operations and locators, tests, test data and testresults.
3. The framework has built-in functionality to measure elapsed time for API requests which can be used for further performance analysis.

## Known Issues
1. "System name" device property is not unique per system and can cause ambiguous recognition. One of possible solutions is to setup MITM proxy and intercept HTTP response to parse out id of the created device.
2. "System type" for existing devices can be "WINDOWS_WORKSTATION" or "WINDOWS WORKSTATION'. This needs to be treated in the test validating devices.