
"""

Hand Detection module
made by :- Pritam
email:- pritambasak024@gmail.com
github:- github.com/Pritam-Basak

"""



import cv2
import mediapipe as mp

class detect:
    def __init__(self,mode=False,maxHands=2,minDetectCon=0.5,minTrackCon=0.5):
        self.static_image_mode=mode
        self.max_num_hands=maxHands
        self.min_detection_confidence=minDetectCon
        self.min_tracking_confidence=minTrackCon

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.static_image_mode,self.max_num_hands,
                                        self.min_detection_confidence,self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.handTips = [4,8,12,16,20]

    def findHands(self,img,draw=True):
        imgrgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(imgrgb)
        if self.results.multi_hand_landmarks : 
            if draw:
                for lndm in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img,lndm,self.mphands.HAND_CONNECTIONS)	 
        return img

    def getPosition(self,img,handNo=0,draw=True):
        self.list = []
        if  self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id ,lnd in enumerate(hand.landmark):
                h,w,_=img.shape
                x = int(lnd.x*w)
                y = int(lnd.y*h)
                self.list.append([id,x,y])
                # if id == 0 & draw==False:
                #     cv2.circle(img,(x,y),15,(255,0,255),cv2.FILLED)
        return self.list

    def handsUp(self):
        hands = []
        if self.list[self.handTips[0]][1] > self.list[self.handTips[0]-1][1]:
            hands.append(1)
        else:
            hands.append(0)
        for id in range(1,5):
            if self.list[self.handTips[id]][2] < self.list[self.handTips[id]-2][2]:
                hands.append(1)
            else:
                hands.append(0)
        return hands
 


