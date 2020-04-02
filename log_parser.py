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

# I got rate limited on the free ipapi version, this allows for an optional query paramter to use an API key stored as an env var. 
ip_api_key = os.getenv('IPAPI_KEY') 
if ip_api_key is not None:
	ip_location_suffix += "?key=" + ip_api_key

csv_name = "location_to_device.csv"
output_path = cwd + "/" + csv_name
column_descriptions = ["Country", "State", "Device", "Browser"]

def get_location(url: str) -> {}:
	response = requests.get(url)
	if response.status_code == 200:
		json_response = response.json()
		country = json_response['country_name']
		region = json_response['region']
		return {'country' : country, 'region': region}
	return {}

def get_device(ua: str) -> {}:
	params = {
		'access_key': userstack_key,
		'ua' : ua
	}
	response = requests.get(userstack_url, params)
	if response.status_code == 200:
		json_response = response.json()
		device_type = json_response['device']['type']
		browser = json_response['browser']['name']
		return {'type' : device_type, 'browser': browser}
	return {}

with open(target_path, "r") as target, open(output_path, "w", newline = "") as output:
	print("Looking up locations and devices for access log")
	writer = csv.writer(output)
	writer.writerow(column_descriptions)
	
	for line in target:
		ip = line.split(" ")[0]
		print(ip)
		user_agent = line.rsplit("\"")[-2]

		ip_location_url = ip_location_base_url + ip + ip_location_suffix
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
