import utils
from MotorModule import Motor
import RoadModule as Rm
import cv2, numpy as np

##################################################
motor = Motor(2,3,4,16,20,21)
##################################################
 
def main():
    trip()    # andata
    turnAround()# turnAround    
    trip()  # ritorno
    motor.stop(1)
    print('The end')

def trip():
    blackFrames = 0
    cap = cv2.VideoCapture(0)
    #initalTrackbarVals = [56, 131, 0, 240]
    #utils.initializeTrackbars(initalTrackbarVals)
    #count_nyStop = [0, 0]
    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:

            img = img[150:-12] # crop
            img = cv2.resize(img,(480,240))

            '''isStop = utils.stopDetector(img,'cascade.xml', 1200)
            count_nyStop[isStop] += 1
            if count_nyStop[1] > 15:
                    count_nyStop[0] = 0
                    motor.stop(2)
                    motor.move(0.2, 0, 0.3)
            elif count_nyStop[0] > 10:
                    count_nyStop[1] = 0'''
            
            perceivedW = utils.stopDetector(img,'cascade.xml', 1200)
            distance3D = utils.distance_to_camera(perceivedW)
            if 10 < distance3D < 15:
                motor.stop(2)
                motor.move(0.2, 0, 0.3)
            dist, isEnded = Rm.getLaneCurve(img, display=0)

            if isEnded: blackFrames += 1 
            else: blackFrames = 0
            
            if blackFrames > 8: break

            motor.move(0.2,-dist,0.01)

            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
     
def turnAround():
    motor.move(0.2, 0, 0.6)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img[150:-12],(480,240))
            imgThres = utils.thresholding(img)

            hT, wT = img.shape[:2]
            points = np.float32([(106, 111), (480-106, 111), (24 , 223), (480-24, 223)])
            eagleView = utils.warpImg(imgThres,points,wT,hT)

            if not Rm.RoadEnded(eagleView):
                break
            motor.parkour()

if __name__ == '__main__':
    main()
