#!/usr/bin/env python3
from queue import Queue
from threading import Thread


q = Queue(maxsize=1)


def worker():
    print("Work")
    item = q.get()
    print("Work done was: ", do_work(item))
    q.task_done()
    

def do_work(item):
    return (item, item*item)




if __name__ == '__main__':
    worker_t = Thread(target=worker)
    worker_t.deamon = True
    worker_t.start()

    q.put(3)
    q.join()
