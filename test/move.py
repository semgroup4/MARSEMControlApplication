import requests
import time

s = requests.Session()
totaltime = 0
runtime = 0

x = range(0,100)


for i in x:
    t = time.time()
    r = s.get("http://192.168.2.1:8000/", params={"action": "forward"}, headers={"Content-Type": "application/json"})
    runtime = time.time() - t
    totaltime += runtime


print("Time to perform 100 requests: ", totaltime)
print("AVG requests per counter: ", totaltime/100)
