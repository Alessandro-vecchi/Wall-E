from MotorModule import Motor
from RoadModule import getLaneCurve
import cv2
 
##################################################
motor = Motor(2,3,4,16,20,21)
##################################################
 
def main():
    trip()    # andata
    motor.parkour() # turnAround
    trip()  # ritorno

def trip():
    cap = cv2.VideoCapture(0)
    #initalTrackbarVals = [56, 131, 0, 240]
    #utils.initializeTrackbars(initalTrackbarVals)
    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            img = img[150:-12] # crop
            img = cv2.resize(img,(480,240))
            dist, isEnded = getLaneCurve(img, display=0)
            
            if isEnded:
                break
            motor.move(0.2,-dist,0.01)

            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
    motor.stop()
     
 
if __name__ == '__main__':
    main()
