import Extras.Webcam as wC
import DataCollection as dC
import Extras.JoyStick as jS
import MotorModule as mM
import cv2
from time import sleep


maxThrottle = 0.25
motor = mM.Motor(2,3,4,16,20,21)

record = 0
while True:
    joyVal = jS.getJS()
    #print(joyVal)
    steering = joyVal['axis0']
    throttle = joyVal['o']*maxThrottle
    if joyVal['share'] == 1:
        if record == 0: print('Recording Started ...')
        record +=1
        sleep(0.300)
    if record == 1:
        img = wC.getImg(False)
        dC.saveData(img,steering)
    elif record == 2:
        dC.saveLog()
        record = 0

    motor.move(throttle, -steering)
    cv2.waitKey(1)