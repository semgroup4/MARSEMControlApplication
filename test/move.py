import marsem.protocol.car as car
import time

counter = 0
t = time.time() + 60
while True:
    time.sleep(0.05)
    counter += 1
    if counter % 2 == 0:
        car.move_right()

    car.move_forward()
    if time.time() > t:
        break
