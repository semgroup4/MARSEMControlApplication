#!/usr/bin/env python

config = {
    "host": "localhost",
    "port": "8000",
    "headers": {"Content-Type": "application/json"},
    "stream-port": "2222",
    "remote-user": "pi",
    "remote-p": "raspberry",
}

host_index = "http://" + config['host'] + ":" + config['port']
host_stream = "http://" + config['host'] + "/stream/" + ":" + config['port']
