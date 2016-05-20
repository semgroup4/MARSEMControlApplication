#!/usr/bin/env python

config = {
    "host": "192.168.2.1",
    "port": "8000",
    "headers": {"Content-Type": "application/json"},
    "stream-port": "2222",
}

host_index = "http://" + config['host'] + ":" + config['port']
host_stream = "http://" + config['host'] + ":" + config['port'] + "/stream/"
stream_file = "tcp://" + config['host'] + ":" + config['stream-port']
host_picture = "http://" + config['host'] + ":" + config['port'] + "/picture/"
