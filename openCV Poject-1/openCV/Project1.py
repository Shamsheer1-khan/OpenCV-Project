import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [[5,107,0,19,255,255],
           [133,56,0,159,156,255],
           [57,76,0,100,255,255],
            [90,48,0,118,255,255]]

mycolorValues=[[51,153,255],
               [255,0,255],
               [0,255,0],
               [255,0,0]]

myPoints = []


def findColor(img,myColors,mycolorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:

        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getCountours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]), mask)
    return newPoints


def getCountours(img):
    countours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = 0,0,0,0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawonCanvas(myPoints,mycolorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,mycolorValues[point[2]],cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints=findColor(img,myColors,mycolorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawonCanvas(myPoints,mycolorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break