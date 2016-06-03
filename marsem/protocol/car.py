#!/usr/bin/env

import requests
import json
import time
from threading import Thread, current_thread
import queue

import marsem.protocol.config as cfg
import paramiko
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException
from requests.exceptions import Timeout, HTTPError, ConnectionError
import socket
from functools import partial

# This queue is filled with move commands
pq = queue.PriorityQueue(maxsize=6)
# Priority of the commands.
prios = {
    "forward": 2,
    "backward": 2,
    "right": 1,
    "left": 1
}
# session
session = requests.Session()
# SSH Client
ssh = paramiko.client.SSHClient()
# Warning
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # There be dragons here, do not use with untrusted hosts!


# The exported functions from this module
__all__ = ['move_left','move_right','move_forward', 'move_backward', 'stream', 'picture', 'status', 'start_server', 'stop_server', 'stop_move_thread']

# **************************************
# Server commands
# These are the exported commands!
# Only use these outside of this module.
# **************************************
def move_left():
    return move_car(action="left")


def move_right():
    return move_car(action="right")


def move_forward():
    return move_car(action="forward")


def move_backward():
    return move_car(action="backward")


def stream(t, success=None, failure=None):
    """ Tells the car server to start or stop streaming. 
    t is a boolean indicating if the server should start or stop streaming, False | True 
    success is a callback function if the stream started successfully.
    failure is for when the stream fails to stop or start."""
    return base_request(partial(stream_f, t, success=success,failure=failure), 
                        (Timeout, HTTPError, ConnectionError))

def picture():
    """ Captures a picture with the car camera and returns the picture in a binary format. """
    return base_request(partial(picture_f), 
                        (Timeout, HTTPError, ConnectionError))

def status():
    """ Gets the status of the server, return a dictionary of the various statuses, {server: True, stream: False} as an example. """
    return base_request(partial(status_f), 
                        (Timeout, HTTPError, ConnectionError))

def start_server():
    """ Starts the server using an SSH client to run the commands to start the server if the server is not running. """
    return base_ssh_request(partial(start_server_f), (BadHostKeyException, AuthenticationException, SSHException, socket.error))

def stop_server():
    """ Runs the command to kill the server if the server is running. """
    return base_ssh_request(partial(stop_server_f), (BadHostKeyException, AuthenticationException, SSHException, socket.error))

def stop_move_thread():
    global command_thread
    if command_thread:
        queue.join()
        command_thread.join()

# **************************************
# Base commands
# Do not use these outside of this module!
# **************************************
def move_car(action=None):
    """ Moves the car, puts the command on the queue and then performs one command at a time.
    This to ensure we don't flood the the server with requests.
    This function is threaded."""
    try:
        pq.put((prios[action], action, 3), timeout=0.5)
        worker = Thread(target=move, daemon=True)
        worker.start()
    except queue.Full as e:
        pass

# desc: sends a move action to the Car
def move():
    global session
    global pq
    # Always gets the most important thing in the queue first
    action = pq.get() # action is a tuple, 0 is prio, 1 is data
    try:
        for x in range(0, action[2]):
            r = session.get(cfg.host_index, 
                            params={"action": action[1]}, 
                            headers=cfg.config['headers'], 
                            timeout=0.5)
        pq.task_done()
    except (Timeout, HTTPError, ConnectionError) as error:
        pq.task_done()
   
def stream_f(run, success=None, failure=None):
    global session
    r = session.get(cfg.host_stream, params={"stream": run}, headers=cfg.config['headers'], timeout=5)
    if (r.status_code == 200):
        response = r.json()
        if success != None:
            success(response['running'])
            return response['running']
        else:
            return response['running']
    else:
        if failure != None:
            failure(False)
        else:
            return False



def picture_f():
    global session
    """ Returns a boolean if it fails and a binary picture if it succeds. """
    r = session.get(cfg.host_picture, params={"picture": True}, headers=cfg.config['headers'], timeout=20)
    if (r.status_code == 200):
        return r.content
    else:
        return False



def status_f():
    global session
    """ Returns a boolean if it fails and a dictionary {} if it succeds. """
    r = session.get(cfg.host_status, params={"status": True}, headers=cfg.config['headers'], timeout=5)
    if (r.status_code == 200):
        return r.json()
    else:
        return False


def start_server_f():
    """ Returns a boolean if the server is running or not. """
    ssh.connect(cfg.config['host'], username="pi", password="raspberry", timeout=5.0)
    stdin, stdout, stderr = ssh.exec_command("pgrep python3")
    if len(stdout.readlines()) == 0:
        stdin, stdout, stderr = ssh.exec_command("python3 marsem/server/main.py &")
        # Read stdout? For success?
        ssh.close()
        return True
    else:
        ssh.close()
        return True
    return False

def stop_server_f():
    def format_value(x):
        """ Removes newlines in the value returned by running pgrep on the remote. """
        return x.strip("\n")
    """ Returns a boolean if the server is running or not, it will also stop the server if it is running. """
    ssh.connect(cfg.config['host'], username="pi", password="raspberry")
    stdin, stdout, stderr = ssh.exec_command("pgrep python")
    res = stdout.readlines()
    print(res)
    if len(res) >= 1:
        res = format_value(res[0])
        stdin, stdout, stderr = ssh.exec_command("kill -s SIGTERM " + res)
        ssh.close()
        return True
    else:
        ssh.close()
        return True
    return False

# **************************************
# Generic commands
# Do not export these!
# **************************************

def base_request(f, exceptions):
    try:
        return f() # This is a function that returns a boolean value
    except exceptions as error:
        return False

def base_ssh_request(f,exceptions):
    try:
        return f()
    except exceptions as error:
        return False


