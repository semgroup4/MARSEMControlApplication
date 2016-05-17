#!/usr/bin/env

import requests
from threading import Thread
from queue import Queue

import marsem.protocol.config as cfg
import paramiko

# This queue is filled with move commands
queue = Queue(maxsize=1)
ssh = paramiko.cient.SSHClient()
# Warning
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # There be dragons here, do not use with untrusted hosts!
ssh.load_system_keys()

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
        return True
    else:
        return False

    
def start_server():
    try:
        ssh.connect("192.168.2.1", username="pi", password="raspberry")
        stdin, stdout, stderr = ssh.exec_command("ps cax | grep python3")
        stdin, stdout, stderr = ssh.exec_command("python3 marsem/server/main.py &")
        return True
    except SSHException as error:
        print(error)
        return False
