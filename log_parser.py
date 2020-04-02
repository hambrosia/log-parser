#!/usr/bin/python3

import os
import requests

cwd = os.getcwd()
file_path = cwd + "/" + "example.log"

userstack_key = os.getenv('USERSTACK_KEY')
userstack_url = "http://api.userstack.com/detect"

ip_location_base_url = "https://ipapi.co/"
ip_location_suffix = "/json"

def get_location(url: str) -> {}:
	ip_location_response = requests.get(url).json() 
	country = ip_location_response['country_name']
	region = ip_location_response['region']
	return {"country" : country, "region": region}

def get_device_browser(ua: str) -> {}:
	params = {
		'access_key': userstack_key,
		'ua' : ua
	}
	useragent_response = requests.get(userstack_url, params).json()
	device = useragent_response['device']['type']
	browser = useragent_response['browser']['name']
	return {"device" : device, "browser": browser}
 	
with open(file_path, "r") as file:
	for line in file:
		ip = line.split(" ")[0]
		user_agent = line.rsplit("\"")[-2]
		ip_location_url = ip_location_base_url + ip + ip_location_suffix
		location = get_location(ip_location_url)
		print(str(location))
		device_browser = get_device_browser(user_agent)
		print(str(device_browser))	

