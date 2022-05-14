import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture("tcp://192.168.0.22:5555")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    t = time.process_time()
    ret, frame = cap.read()
    elapsed_time = time.process_time() - t
    print(elapsed_time*1000) # ms
    time.sleep(0.05)
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()