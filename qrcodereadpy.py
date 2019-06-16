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

cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',port='3307' , database='drivepark')

#print('hello')
mycursor = cnx.cursor()
mycursor.execute("SELECT * FROM  clients")
myresult = mycursor.fetchall()

qrliste = []
data = []

for x in myresult:
   qrliste.append(x[3])
   #data.append[x[1],x[2]]
   print(x[3])

for i,el in enumerate(qrliste):
    fmt = 'b\''+el+'\''
    qrliste[i] = fmt
#print("b'1234567'" in qrliste)
#print(qrliste[0])



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
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        # Number of points in the convex hull
        n = len(hull)
        # Draw the convext hull
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)
        #print(decodedObject.data[1:])

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,str(decodedObject.data) ,'\n')
        if str(decodedObject.data) in qrliste:
            print("XXXXXXXXXXXXX-XXXXXXXXXXXXXX [acccess] Hello XXXXXXXXXXXXX-XXXXXXXXXXXXXXXX")
           
            r = requests.get("http://192.168.43.118/action")  #envoi requete arduino
            envoi()    #envoi sur firebase
           # print(r)
            token = True
            break
        else : token = False

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):  # wait for 's' key to save
        cv2.imwrite('Capture.png', frame)

    # When everything done, release the capture
    
cap.release()

cv2.destroyAllWindows()



cnx.close()


