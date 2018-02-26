import json
import requests


def post(url, data, username=None, password=None):
    headers = {
        'Content-Type': 'application/json',
        'Accepts': 'application/json'
    }

    response = requests.post(url=url, headers=headers, data=data, auth=(username, password))

    return response