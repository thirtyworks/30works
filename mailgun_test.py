import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)

import requests
def send_simple_message():
    	return requests.post(
		"https://api.eu.mailgun.net/v3/30works.thirty.works/messages",
		auth=("api", config_json["MAILGUN_API"]),
		data={"from": "info@thirty.works",
			"to": ["",],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})
send_simple_message()

