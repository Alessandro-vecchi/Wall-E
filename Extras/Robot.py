from MotorModule import Motor
import KeyPressModule as kp
import cv2

motor = Motor(2,3,4,16,20,21)

kp.init()

def main():
    if kp.getKey('w'):
        motor.move(0.2)
    elif kp.getKey('s'):
        motor.move(-0.2)
    elif kp.getKey('d'):
        motor.move(0.2,-0.1)
    elif kp.getKey('a'):
        motor.move(0.2,0.1)
    else:
        motor.stop()

if __name__ == '__main__':
    while True:
        main()
        if kp.getKey('p'):
            kp.Quit()
            break
