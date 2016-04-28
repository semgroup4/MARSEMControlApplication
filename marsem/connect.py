#!/usr/bin/env

import requests

# Server IP & Port
# CAR IP: 192.168.2.1
config = {
    "host": "localhost",
    "port": "8000",
    "headers": {"Content-Type": "application/json"},
}

host = "http://" + config['host'] + ":" + config['port']

# desc: sends a move action to the Car
def move(action=None):
    r = requests.get(host, params={"action": action}, headers=config['headers'])
    return r.text;
