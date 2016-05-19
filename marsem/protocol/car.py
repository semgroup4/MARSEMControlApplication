#!/usr/bin/env

import requests

import marsem.protocol.config as cfg

from threading import Thread
from queue import Queue

# This queue is filled with move commands
queue = Queue(maxsize=1)


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


def picture():
    """ Returns an image binary captured from the raspberry pi camera.
    Encoding is JPEG."""
    r = requests.get("http://localhost:8000/picture",params={"picture": True}, headers=cfg.config['headers'])
    if (r.status_code == 200):
        return r.content
    else:
        return False
