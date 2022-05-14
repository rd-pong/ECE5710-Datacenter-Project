import cv2
import time
from pyardrone.video import VideoClient
import timeit

import logging

logging.basicConfig(level=logging.DEBUG)

client = VideoClient('192.168.1.1', 5555)
client.connect()
client.video_ready.wait()

try:
    while True:
        t = time.process_time()
        cv2.imshow('im', client.frame)
        elapsed_time = time.process_time() - t
        print(elapsed_time*1000) # ms
        time.sleep(0.5)

        if cv2.waitKey(10) == ord(' '):
            break
finally:
    client.close()
    