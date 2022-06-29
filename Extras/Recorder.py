from MotorModule import Motor
import KeyPressModule as kp
import cv2
motor = Motor(2,3,4,16,20,21)

kp.init()

def main():
    
    video = cv2.VideoCapture(0)

    if (video.isOpened() == False): 
        print("Error reading video file")
        
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
       
    size = (frame_width, frame_height)
    result = cv2.VideoWriter('thor2.avi', cv2.VideoWriter_fourcc(*'MJPG'),30, size)
    while(True):
        ret, frame = video.read()
        
        if ret == True:
            if kp.getKey('w'):
                motor.move(0.2)
            elif kp.getKey('s'):
                motor.move(-0.2)
            elif kp.getKey('d'):
                motor.move(0.2,-0.2)
            elif kp.getKey('a'):
                motor.move(0.2,0.2)
            elif kp.getKey('p'):
                kp.Quit()
                break
            else:
                motor.stop()
          
            result.write(frame)
     
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
      
        else:
            break
      
    video.release()
    result.release()
    cv2.destroyAllWindows()
    print("The video was successfully saved")
    
if __name__ == '__main__':
    #while True:
    main()
