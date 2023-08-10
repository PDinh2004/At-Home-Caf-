import requests
import json
import random


def fetchQuote():
    try:
        response_API = requests.get('https://zenquotes.io/api/quotes')

        data = response_API.text

        parse_JSON = json.loads(data)

        return random.choice(parse_JSON)
    except:
        print("Failed to load quotes")
