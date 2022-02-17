import os
import json
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join('30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)

html_message = open('./email_templates/daily_brief.html').read()


def send_simple_message():
    	return requests.post(
		"https://api.eu.mailgun.net/v3/30works.thirty.works/messages",
		auth=("api", config_json["MAILGUN_API"]),
		data={"from": "30works <info@thirty.works>",
			"to": [""],
			"subject": "30works30days DAY 0 Brief",
			"text": "Testing some Mailgun awesomness!",
			"html": html_message })
x = send_simple_message()

print(x.text)

