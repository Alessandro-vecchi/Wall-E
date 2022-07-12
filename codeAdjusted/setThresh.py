import cv2, numpy as np


def empty(h):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179,  empty)
cv2.createTrackbar("SAT Min", "HSV", 15, 255,  empty)
cv2.createTrackbar("SAT Max", "HSV",108, 255,  empty)
cv2.createTrackbar("VAL Min", "HSV", 200, 255,  empty)
cv2.createTrackbar("VAL Max", "HSV",255, 255,  empty)

framec = 0
cap = cv2.VideoCapture("/Users/alessandrovecchi/Downloads/percorsoCam.mp4")
while True:
    framec += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == framec:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        framec=0
    succ, img = cap.read()
    if succ == True:
        img = img[150:-12]
        img = cv2.resize(img,(480,240))

        imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("HUE Min", "HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VAL Min", "HSV")
        v_max = cv2.getTrackbarPos("VAL Max", "HSV")

        lowerWhite = np.array([h_min, s_min, v_min])
        upperWhite = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHSV, lowerWhite, upperWhite)
        result = cv2.bitwise_and(img, img, mask=mask)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        hstack = np.hstack([img, mask, result])
        cv2.imshow('stack', hstack)
        if cv2.waitKey(1) == ord("q"):
            print(s_min,s_max,v_min,v_max)
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()