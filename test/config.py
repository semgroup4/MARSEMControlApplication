config = {
    "host": "localhost",
    "port": "8000",
    "headers": {"Content-Type": "application/json"},
    "stream-port": "2222",
}

host_index = "http://" + config['host'] + ":" + config['port']
host_stream = "http://" + config['host'] + ":" +config['port'] + "/stream/"
stream_file = 0
