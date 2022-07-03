import cv2
import numpy as np


def thresholding(img):
    img = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([0,0,201])
    upperWhite = np.array([179,110,255])
    maskWhite = cv2.inRange(imgHsv,lowerWhite,upperWhite)
    return maskWhite


def warpImg(img,points,w,h,inv = False):
    pts1 = np.float32(points)
    pts2 =  np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2,pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    return imgWarp

def nothing(a):
    pass


def initializeTrackbars(intialTracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)


def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points


def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(255,0,0),cv2.FILLED)
    return img


def getHistogram(img,display=False,minPer = 0.1,region= 1):
    h, w = img.shape[:2]
    histValues = np.sum(img[-h//region:,:], axis=0)

    maxValue = np.max(histValues)  # FIND THE MAX VALUE
    minValue = minPer*maxValue

    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))

    if display:
        imgHist = np.zeros((h, w, 3),np.uint8)
        for x, intensity in enumerate(histValues):
        # print(intensity)
            if intensity > minValue:color=(211,211,211)
            else: color=(200,165,200)
            cv2.line(imgHist,(x,h),(x,int(h-(intensity//region//255))),color,1)
            cv2.circle(imgHist,(basePoint,h),20,(255,200,0),cv2.FILLED)
        return basePoint, imgHist
    
    return basePoint


def stackImages(scale, imgArray):

    if isinstance(imgArray[0], list):
        return imageMatrix(scale, imgArray)
    return imageArray(scale, imgArray)

def imageMatrix(scale, imgArray):
    rows, cols = len(imgArray), len(imgArray[0])

    hImg, wImg = imgArray[0][0].shape[:2]

    for x in range(0, rows):
        for y in range(0, cols):
            imgArray[x][y] = cv2.resize(imgArray[x][y], (int(wImg*scale), int(hImg*scale)), None)
            if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

    imageBlank = np.zeros((hImg, wImg, 3), np.uint8)
    hor = [imageBlank]*rows
    for x in range(0, rows):
        hor[x] = np.hstack(imgArray[x])

    return np.vstack(hor)


def imageArray(scale, imgArray):

    for x in range(0, len(imgArray)):

        imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)

        if len(imgArray[x].shape) == 2: 
            imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)

    return np.hstack(imgArray)


def stopDetector(img,cascadePath, minArea):
    cascade = cv2.CascadeClassifier(cascadePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scaleVal = 1 + 161/1000
    neig = 11
    objects = cascade.detectMultiScale(gray, scaleVal, neig)
    for (x,y,w,h) in objects:
        area = w*h
        if area > minArea:
            return w
    return 0


def distance_to_camera(perWidth):
    # https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
	# compute and return the distance from the marker to the camera
    knownWidth = 5 # width stop sign
    focalLength = 2 # to be obtained
    '''
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	cv2.putText(image, "%.2fft" % (inches / 12),
		(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		2.0, (0, 255, 0), 3)'''
    return (knownWidth * focalLength) / perWidth

