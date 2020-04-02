# Log Parser
Log Parser is a Python implementation of a log parser, intended to take log files and provide useful information or insights.

## Requirements and Installation
* Ensure Python interpreter is located at: `/usr/bin/python3` or update shebang in `log_parser.py` to reference the location of the interpreter on your system.
* Ensure the script is executable. `chmod 755 log_parser.py` or `chmod + log_parser.py` allows execution
* Install requirements from `requirements.txt` using `pip` or simply `pip3 install requests` as it is the only dependency at this time.
* Create an account with Userstack (userstack.com). Retrieve your API key and export it. `export USERSTACK_KEY=<your_key_here>`

## Current Features
The current version has support for the following log file formats and functions:

* Supported formats: NGINX access logs
* Supported functions: print approximate location (Country, State), device type (Mobile, Desktop, Tablet), and browser (Chrome, Firefox, Safari, etc.) to a CSV file.

