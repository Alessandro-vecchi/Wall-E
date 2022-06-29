import cv2
import utils
img = cv2.VideoCapture(0)

while True:
    ret, frame = img.read()
    frame = frame[150:-12]
    frame = cv2.resize(frame,[480,240])
    cv2.imshow('Live',frame)
    cv2.imshow('threshhh',utils.thresholding(frame))
    if cv2.waitKey(1) == ord('q'):
        break
    
img.release()
cv2.destroyAllWindows()
