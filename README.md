# Log Parser
Log Parser is a Python implementation of a log parser, intended to take log files and provide useful information or insights.

## Requirements and Installation
* Ensure Python interpreter is located at: `/usr/bin/python3` or update shebang in `log_parser.py` to reference the location of the interpreter on your system.
* Ensure the script is executable. `chmod 755 log_parser.py` or `chmod +x log_parser.py` allows execution
* Install requirements from `requirements.txt` using `pip` or simply `pip3 install requests` as it is the only dependency at this time.
* Create an account with Userstack (userstack.com). Retrieve your API key and export it. `export USERSTACK_KEY=<your_key_here>`
* (Optional): If you have a purchased API key for IPAPI (https://ipapi.co/) you can export it using `export IPAPI_KEY=<your_key_here>`. This helps to avoid rate limiting issues.

## Current Features
The current version has support for the following log file formats and functions:

* Supported formats: NGINX access logs
* Supported functions: print approximate location (Country, State), device type (Mobile, Desktop, Tablet), and browser (Chrome, Firefox, Safari, etc.) to a CSV file.

## Usage
* Target log file must be NGINX access log format, e.g.: `75.114.153.6 - - [10/Jun/2015:18:14:56 +0000] "GET /favicon.ico HTTP/1.1" 200 0 "http://www.gobankingrates.com/banking/find-cds-now/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"`
* Run script using standard `./` syntax followed by the path to the log, i.e. `./log_parser.py ~/log-parser/target.log`
* Result will be printed to a file in the same directory called `location_to_device.csv`
