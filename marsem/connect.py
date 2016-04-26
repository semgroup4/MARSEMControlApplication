#!/usr/bin/env
# author: phcr
# The API to tell the car how to operate.
import httplib, urllib

# Server IP & Port
# CAR IP: 192.168.2.1
config = {
    "host": "localhost",
    "port": "8000",
    "headers": {"Content-Type": "application/json"},
}

# Connect to the server, creates a HTTPConnection type
connection = httplib.HTTPConnection(config['host'], config['port'])

connection.connect()
# desc: sends a move action to the Car
# returns: HTTPResponse Object
# docs: https://docs.python.org/2/library/httplib.html#httpresponse-objects
def move(action=None):
    connection.request("GET", "/", params(action), config['headers'])
    return connection.getresponse()


# desc: gets the current status of the Car @NotImplemented
# returns: HTTPResponse Object
# docs: https://docs.python.org/2/library/httplib.html#httpresponse-objects
def status():
    connection.request("GET", "/status")
    return connection.getresponse()


def params(param):
     return urllib.urlencode({"action": param})
