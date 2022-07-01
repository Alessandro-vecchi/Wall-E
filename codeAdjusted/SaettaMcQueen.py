import utils
from MotorModule import Motor
from RoadModule import getLaneCurve
import cv2
from time import sleep

##################################################
motor = Motor(2,3,4,16,20,21)
##################################################
 
def main():
    trip()    # andata
    motor.move(0.2,0,0.28)
    motor.parkour(t=0.95)
    motor.stop(0.4) 
    sleep(0.4)# turnAround    
    trip()  # ritorno
    motor.stop(1)
    print('the end')

def trip():
    endlist = []
    cap = cv2.VideoCapture(0)
    #initalTrackbarVals = [56, 131, 0, 240]
    #utils.initializeTrackbars(initalTrackbarVals)
    cf = 0
    cstops = 0
    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            cf = (cf +1)%30
            if cf == 0: cstops = 0

            img = img[150:-12] # crop
            img = cv2.resize(img,(480,240))

            if cf % 2:
                cstops += utils.stopDetector(img,'cascade.xml')

            if cstops >= 5:
                motor.stop(2)
                cstops=0
            dist, isEnded = getLaneCurve(img, display=0)
            endlist.append(isEnded)
            if sum(endlist) > 10:
                break
            motor.move(0.2,-dist,0.01)

            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
     
 
if __name__ == '__main__':
    main()
