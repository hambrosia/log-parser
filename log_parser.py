#!/usr/bin/python3

import csv
import os
import sys
import requests

# Output filepaths and formatting
CWD = os.getcwd()
CSV_NAME = "location_to_device.csv"
OUTPUT_PATH = CWD + "/" + CSV_NAME
COLUMN_DESCRIPTIONS = ["Country", "State", "Device", "Browser"]

# Required Userstack API key:
def userstack_api_key() -> str:
    userstack_api_key = os.getenv('USERSTACK_KEY')
    if userstack_api_key is not None:
        return userstack_api_key
    print("Rquired Userstack API key not found in environment variables. Export key as USERSTACK_KEY")
    sys.exit(os.EX_CONFIG)

USERSTACK_KEY = userstack_api_key()
USERSTACK_URL = "http://api.userstack.com/detect"

# Optional IPAPI key added if present
def ip_api_suffix() -> str:
    ip_location_suffix = "/json"
    ip_api_key = os.getenv('IPAPI_KEY')
    if ip_api_key is not None:
        ip_location_suffix += "?key=" + ip_api_key
    return ip_location_suffix

IP_API_BASE_URL = "https://ipapi.co/"
IP_API_SUFFIX = ip_api_suffix()

# Validate arguments and filepath
def argument_exists() -> bool:
    exists = False
    if len(sys.argv) > 1:
        exists = True
    return exists

def target_exists(path: str) -> bool:
    return os.path.exists(path)

def exit_no_input() -> None:
    print("Target not found at specified path. Ensure correct path to target is passed as argument. \nExample usage:  ./log_parser.py <path to file>")
    sys.exit(os.EX_NOINPUT)

def get_target_path() -> str:
    if argument_exists():
        if target_exists(sys.argv[1]):
            return sys.argv[1]
    exit_no_input()
    return ""

TARGET_PATH = get_target_path()

# Request location using IP
def get_location(url: str) -> {}:
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        country = json_response['country_name']
        region = json_response['region']
        return {'country' : country, 'region': region}
    return {}

# Request device information using useragent
def get_device(useragent: str) -> {}:
    params = {
        'access_key': USERSTACK_KEY,
        'ua' : useragent
    }
    response = requests.get(USERSTACK_URL, params)
    if response.status_code == 200:
        json_response = response.json()
        device_type = json_response['device']['type']
        browser = json_response['browser']['name']
        return {'type' : device_type, 'browser': browser}
    return {}

def convert_log_to_csv() -> None:
    with open(TARGET_PATH, "r") as target, open(OUTPUT_PATH, "w", newline = "") as output:
        print("Looking up locations and devices for access log")
        writer = csv.writer(output)
        writer.writerow(COLUMN_DESCRIPTIONS)

        for line in target:
            ip_addr = line.split(" ")[0]
            print(ip_addr)
            user_agent = line.rsplit("\"")[-2]

            ip_location_url = IP_API_BASE_URL + ip_addr + IP_API_SUFFIX
            location = get_location(ip_location_url)
            if location == {}:
                print("No location or bad response, skipping entry")
                continue
            print("Location: " + location['country'] +  " Region: " + location['region'])

            device = get_device(user_agent)
            if device == {}:
                print("No device or bad response, skipping entry")
                continue

            print("Device Type: " + device['type'] +  " Browser: " + device['browser'])

            writer.writerow([location['country'], location['region'], device['type'], device['browser']])

    print("Complete! CSV file written to location_device.csv")

def main() -> None:
    convert_log_to_csv()
    sys.exit(os.EX_OK)

if __name__ == "__main__":
    main()
