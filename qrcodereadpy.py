from __future__ import print_function

import mysql.connector
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import requests
from fbcon import envoi  

token = False
r = None

## arduino_IP here ##
ip_arduino = ""
cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',port='3307' , database='drivepark')


mycursor = cnx.cursor()
mycursor.execute("SELECT * FROM  clients")
myresult = mycursor.fetchall()

qrliste = []
data = []

for x in myresult:
   qrliste.append(x[3])
   print(x[3])

for i,el in enumerate(qrliste):
    fmt = 'b\''+el+'\''
    qrliste[i] = fmt




# get the webcam:
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
# 160.0 x 120.0
# 176.0 x 144.0
# 320.0 x 240.0
# 352.0 x 288.0
# 640.0 x 480.0
# 1024.0 x 768.0
# 1280.0 x 1024.0
time.sleep(2)


def decode(im):

    decodedObjects = pyzbar.decode(im)

    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened()):

    ret, frame = cap.read()

    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon


        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

     
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)


        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,str(decodedObject.data) ,'\n')
        if str(decodedObject.data) in qrliste:
            print("XXXXXXXXXXXXX-XXXXXXXXXXXXXX [acccess]  XXXXXXXXXXXXX-XXXXXXXXXXXXXXXX")
           
            r = requests.get(f"http://{ip_arduino}action")  
            envoi()    
           # print(r)
            token = True
            break
        else : token = False

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):  # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

 
    
cap.release()

cv2.destroyAllWindows()



cnx.close()


