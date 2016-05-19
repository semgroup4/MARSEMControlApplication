#!/usr/bin/env

import requests
import json
from threading import Thread
from queue import Queue

import marsem.protocol.config as cfg
import paramiko

# Global state variables
SERVER_RUNNING = False

# This queue is filled with move commands
queue = Queue(maxsize=1)
ssh = paramiko.client.SSHClient()
# Warning
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # There be dragons here, do not use with untrusted hosts!

def move_left():
    return move_car(action="left")


def move_right():
    return move_car(action="right")


def move_forward():
    return move_car(action="forward")


def move_backward():
    return move_car(action="backward")


def start_stream():
    return stream(True)


def stop_stream():
    return stream(False)


# desc: sends a move action to the Car
def move(action, q):
    r = requests.get(cfg.host_index, params={"action": action}, headers=cfg.config['headers'])
    # We need a way to know if the server is responding at all, if not. Stop!
    q.get() # remove the action from the queue
    q.task_done()
    
def move_car(action=None):
    if queue.empty():
        worker = Thread(target=move, args=(action, queue,))
        worker.deamon = True
        worker.start()
        queue.put(action)


# desc: starts/stops the camera stream on the Car
# params: run, specifices if to start (True) or stop (False)
def stream(run):
    r = requests.get(cfg.host_stream, params={"stream": run}, headers=cfg.config['headers'])
    if (r.status_code == 200):
        response = json.loads(r.json())
        return response['running']
    else:
        return False


def picture():
    """ Returns an image binary captured from the raspberry pi camera.
    Encoding is JPEG."""
    r = requests.get("http://localhost:8000/picture")
    if (r.status_code == 200):
        return r.content
    else:
        return False

# This should probably be threaded, since the server might not be available,
# Will currently block the main thread when this is executed    
def start_server():
    global SERVER_RUNNING
    if SERVER_RUNNING:
        return SERVER_RUNNING
    else:
        try:
            if ssh.get_transport() == None:
                ssh.connect(cfg.config['host'], username="pi", password="raspberry")
            stdin, stdout, stderr = ssh.exec_command("pgrep python3")
            if len(stdout.readlines()) == 0:
                stdin, stdout, stderr = ssh.exec_command("python3 marsem/server/main.py &")
            SERVER_RUNNING = True
            return True
        except paramiko.SSHException as error:
            print(error)
            SERVER_RUNNING = False
            return False
        finally:
            ssh.close()

def stop_server():
    global SERVER_RUNNING
    if not SERVER_RUNNING:
        return not SERVER_RUNNING
    else:
        try:
            if ssh.get_transport() == None:
                ssh.connect(cfg.config['host'], username="pi", password="raspberry")
            stdin, stdout, stderr = ssh.exec_command("pgrep python")
            res = stdout.readlines()
            if len(res) == 1:
                res = format_value(res[0])
                stdin, stdout, stderr = ssh.exec_command("kill -s SIGTERM " + res)
            SERVER_RUNNING = False
            return True
        except paramiko.SSHException as error:
            print(error)
            SERVER_RUNNING = True
            return False
        finally:
            ssh.close()


def format_value(x):
    return x.strip("\n")
