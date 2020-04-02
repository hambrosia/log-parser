#!/usr/bin/python3

import csv
import os
import requests

cwd = os.getcwd()
target_path = cwd + "/" + "target.log"

userstack_key = os.getenv('USERSTACK_KEY')
userstack_url = "http://api.userstack.com/detect"

ip_location_base_url = "https://ipapi.co/"
ip_location_suffix = "/json"

csv_name = "location_to_device.csv"
output_path = cwd + "/" + csv_name
column_descriptions = ["Country", "State", "Device", "Browser"]

def get_location(url: str) -> {}:
	ip_location_response = requests.get(url).json()
	country = ip_location_response['country_name']
	region = ip_location_response['region']
	return {'country' : country, 'region': region}

def get_device_browser(ua: str) -> {}:
	params = {
		'access_key': userstack_key,
		'ua' : ua
	}
	useragent_response = requests.get(userstack_url, params).json()
	device = useragent_response['device']['type']
	browser = useragent_response['browser']['name']
	return {'device' : device, 'browser': browser}

with open(target_path, "r") as target, open(output_path, "w", newline = "") as output:
	writer = csv.writer(output)
	writer.writerow(column_descriptions)

	for line in target:
		ip = line.split(" ")[0]
		user_agent = line.rsplit("\"")[-2]

		ip_location_url = ip_location_base_url + ip + ip_location_suffix
		location = get_location(ip_location_url)
		print(str(location))

		device_browser = get_device_browser(user_agent)
		print(str(device_browser))

		writer.writerow([location['country'], location['region'], device_browser['device'], device_browser['browser']])

