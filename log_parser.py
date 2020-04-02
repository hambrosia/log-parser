#!/usr/bin/python3

import os

cwd = os.getcwd()
file_path = cwd + "/" + "example.log"

with open(file_path, "r") as file:
	for line in file:
		ip = line.split(" ")[0]
		user_agent = line.rsplit("\"")[-2]
		print(ip)
		print(user_agent)

