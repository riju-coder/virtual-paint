import numpy as np
import detectHand as dh
import cv2
import os

brushThikness = 15
brushColor = (208,99,191)
lineColor = (255,255,255)
lineThikness = 5

filePath = 'Headers'
mylist = os.listdir(filePath)

overlay_list=[]
for path in mylist:
    img = cv2.imread("{filePath}/{path}".format(filePath = filePath, path = path))
    overlay_list.append(img)

header = overlay_list[1]
xp,yp = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1280)
detect = dh.detect(minDetectCon=0.8,maxHands=1)

imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    _,img = cap.read()
    img = cv2.flip(img,1)
    img = detect.findHands(img,draw=True)
    lis = detect.getPosition(draw=True,img=img)
    img[:1280][:158] = header
    if len(lis) != 0:
        finger = detect.handsUp()
        x1,y1 = lis[8][1:]
        x2,y2 = lis[12][1:]

        if finger[1] & finger[2]: #selection mode
            cv2.rectangle(img,(lis[8][1],lis[8][2]),(lis[12][1],lis[12][2]),brushColor,cv2.FILLED)
            if cv2.waitKey(2) & 0xFF == ord('s'):
                print(lis[8],lis[12])
            if y1 < 155:
                if 270 < x1 < 400:
                    header = overlay_list[1]
                    brushColor = (255,0,255)
                elif 150 > x1 > 40:
                    header = overlay_list[3]
                    brushColor = (0,0,0)
                elif 730 > x1 > 630:
                    header = overlay_list[2]
                    brushColor = (248,196,100)
                elif 1020 > x1 > 850:
                    header = overlay_list[0]
                    brushColor = (0,255,0)
            if 1190 < x1 < 1210:
                if 240 < y1 < 260 : brushThikness = 10
                elif 300 < y1 < 320: brushThikness = 15
                elif 360 < y1 < 380: brushThikness = 20
                elif 420 < y1 < 440: brushThikness = 25
                elif 480 < y1 < 500: brushThikness = 30
                elif 640 < y1 < 560: brushThikness = 35
        elif finger[1] & finger[2] == False:  #drawing mode
            cv2.circle(img,(lis[8][1],lis[8][2]),15,brushColor,cv2.FILLED)
            if xp == 0 & yp == 0:
                xp,yp = x1,y1
            xp ,yp = x1,y1
            cv2.line(img,(xp,yp),(x1,y1),brushColor,brushThikness)        
            cv2.line(imgCanvas,(xp,yp),(x1,y1),brushColor,brushThikness)

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)
    cv2.line(img,(1200,250),(1200,550),brushColor,lineThikness)
    count = 10
    for i in range(250,551,60):
        cv2.line(img,(1190,i),(1210,i),brushColor,lineThikness)
        cv2.putText(img,str(count),(1220,i),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0))
        if brushThikness == count:
            cv2.circle(img,(1200,i),8,lineColor,cv2.FILLED)
        count += 5
    cv2.imshow("main",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break	
