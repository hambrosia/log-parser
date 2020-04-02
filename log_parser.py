#!/usr/bin/python3

import os
import requests

cwd = os.getcwd()
file_path = cwd + "/" + "example.log"
ip_location_base_url = "https://ipapi.co/"
ip_location_suffix = "/json"

with open(file_path, "r") as file:
	for line in file:
		ip = line.split(" ")[0]
		user_agent = line.rsplit("\"")[-2]
		#print(ip)
		#print(user_agent)
		ip_location_url = ip_location_base_url + ip + ip_location_suffix
		ip_location_response = requests.get(ip_location_url).json() 
		country = ip_location_response['country_name']
		region = ip_location_response['region']
		print(country, region)
		


