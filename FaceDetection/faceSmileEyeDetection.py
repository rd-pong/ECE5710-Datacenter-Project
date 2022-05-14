import numpy as np
import cv2
import time

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('Cascades/haarcascade_smile.xml')

# latency = []

# for i in range(10):

start_time = time.time()

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('tcp://192.168.0.22:5555')
# cap = cv2.VideoCapture('tcp://192.168.1.1:5555')
cap.set(3,640) # set Width
cap.set(4,480) # set Height

# f = open("facedetection_latency_wifi.txt", "a")
# f = open("facedetection_latency_5G.txt", "a")
f = open("facedetection_latency_local.txt", "a")

ret, img = cap.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
        minNeighbors=5,
        minSize=(5, 5),
        )
    
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        
    
    smile = smileCascade.detectMultiScale(
        roi_gray,
        scaleFactor= 1.5,
        minNeighbors=15,
        minSize=(25, 25),
        )
    
    for (xx, yy, ww, hh) in smile:
        cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)

    
end_time = time.time()

# latency.append(end_time-start_time)

print((end_time-start_time))

f.write(f"{(end_time-start_time)}\n")

cap.release()

# print("avg_latency_frames:", np.mean(latency))



    

    


# cv2.destroyAllWindows()
