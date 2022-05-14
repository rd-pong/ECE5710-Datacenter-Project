import numpy as np
import time
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
 
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('tcp://192.168.0.22:5555')
cap = cv2.VideoCapture('tcp://192.168.1.1:5555')
cap.set(3,640) # set Width
cap.set(4,480) # set Height

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()
 
    # Calculating the fps
 
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    time_latency = new_frame_time-prev_frame_time
    fps = 1/(time_latency)
    prev_frame_time = new_frame_time
    print("time_diff:", time_latency)
 
    # converting the fps into integer
    fps = int(fps)
    print("fps:", fps)
 
    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)
 
    # putting the FPS count on the frame
    cv2.putText(img, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,      
        minSize=(30, 30)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=10,
            minSize=(5, 5),
            )
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
               
        cv2.imshow('video', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
