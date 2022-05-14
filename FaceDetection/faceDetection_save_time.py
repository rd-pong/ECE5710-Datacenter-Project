# Calculate average face saved in 5 secs
import numpy as np
import cv2
import time

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# cap = cv2.VideoCapture('tcp://192.168.0.22:5555')
# cap = cv2.VideoCapture('tcp://192.168.1.1:5555')
cap = cv2.VideoCapture(0)

cap.set(3,640) # set Width
cap.set(4,480) # set Height

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
face_num = []

# Loop times
sum = 10

# Time delay for save photos
time_delay = 5

for i in range(sum):

    count = 0

    start_time = time.time()

    while (time.time()-start_time <= time_delay):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            
            scaleFactor=1.2,
            minNeighbors=5
            ,     
            minSize=(20, 20)
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            count += 1

            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(i) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

    face_num.append(count)

avg_save = np.mean(face_num)
print(face_num)
print("Save {} faces in 5 sec".format(int(avg_save)))
cap.release()
cv2.destroyAllWindows()
