from MotorModule import Motor
from LaneModule import getLaneCurve
import numpy as np
import cv2
 
##################################################
motor = Motor(2,3,4,16,20,21)
##################################################
 
def main():
    cap = cv2.VideoCapture(0)
    #initalTrackbarVals = [56, 131, 0, 240]
    #utils.initializeTrackbars(initalTrackbarVals)
    flag = True
    while(cap.isOpened() and flag):
        ret, img = cap.read()
        if ret == True:
            img = img[150:-12]
            img = cv2.resize(img,(480,240))
            curveVal, RoadCenter, flag = getLaneCurve(img,display=0)
            dist = (RoadCenter - 240)
            s=0.6
            #print(dist)
            if dist >=20:
                dist /= 240
                dist = (np.sqrt(np.log10(abs(dist/4)+1)))
            elif dist < 20:
                dist /= 240
                dist = -(np.sqrt(np.log10(abs(dist/4)+1)))
            else:
                dist=0
            motor.move(0.2,-dist,0.01)

            '''
            sen = 1  # SENSITIVITY
            maxVAl= 0.3 # MAX SPEED
            if curveVal>maxVAl:curveVal = maxVAl
            if curveVal<-maxVAl: curveVal =-maxVAl
            #print(curveVal)
            if curveVal>0:
                sen = 1
                if curveVal<0.2: curveVal=0
            else:
                if curveVal>-0.2: curveVal=0
            motor.move(0.2,-curveVal*sen,0.03)
            #cv2.waitKey(1)
            '''
            #cv2.imshow('Frame', img)
            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
    motor.stop()
     
 
if __name__ == '__main__':
    main()
