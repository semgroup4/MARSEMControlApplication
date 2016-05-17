#!/usr/bin/env

import requests
import marsem.protocol.config as cfg


def move_left():
    return move(action="left")


def move_right():
    return move(action="right")


def move_forward():
    return move(action="forward")


def move_backward():
    return move(action="backward")


def start_stream():
    return stream(True)


def stop_stream():
    return stream(False)


# desc: sends a move action to the Car
def move(action=None):
    r = requests.get(cfg.host_index, params={"action": action}, headers=cfg.config['headers'])


# desc: starts/stops the camera stream on the Car
# params: run, specifices if to start (True) or stop (False)
def stream(run):
    r = requests.get(cfg.host_stream, params={"stream": run}, headers=cfg.config['headers'])
    if (r.status_code == 200):
        return True
    else:
        return False
