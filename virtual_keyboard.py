from typing import final
import cv2
import numpy as np
from time import sleep
import cvzone
from pynput.keyboard import Controller
#import HandTrackingModule
from cvzone.HandTrackingModule import HandDetector
from collections import OrderedDict
cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector= HandDetector(detectionCon=0.8)
finaltext=""
previoustext=""
keys= [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"],
        ["0","1","2","3","4","5","6","7","8","9"]]

def Dup(str):
    return "".join(OrderedDict.fromkeys(str))

keyboard=Controller()
def drawALL(frame,buttonList):
    
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(frame,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(frame,button.text,(x+20,y+65),
        cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return frame
class Button():
     def __init__(self,pos,text,size=[85,85]):
         self.pos=pos
         self.size=size
         self.text=text
         
m=0  
buttonList =[]
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([j*100+50,200*i+50],key))
while True:
    ret,frame =cap.read()
    frame = detector.findHands(frame)
    frame = cv2.resize(frame, (1080,960))
    lndmark,bboxin = detector.findPosition(frame)
    frame =drawALL(frame,buttonList)
    if lndmark:
        
        for button in buttonList:
            x,y=button.pos
            w,h=button.size

            if x< lndmark[8][0]<x+w and y<lndmark[8][1]<y+h:
                cv2.rectangle(frame,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                cv2.putText(frame,button.text,(x+20,y+65),
                cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)

                l,_,_=detector.findDistance(8,12,frame,draw=False)
                print(l)

                
                if l<39:
                    
                    cv2.rectangle(frame,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(frame,button.text,(x+20,y+65),
                    cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    # previoustext=button.text
                    previoustext=previoustext+button.text
                    finaltext=Dup(previoustext)
                    # keyboard.press(button.text)
                    m+=1
                    
                    #sleep(0.1)

    cv2.rectangle(frame,(50,850),(900,950),(175,0,175),cv2.FILLED)
    cv2.putText(frame,finaltext,(100,900),
    cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)





    # keyboard.press(finaltext)
    cv2.imshow("Image",frame)
    cv2.waitKey(1)

