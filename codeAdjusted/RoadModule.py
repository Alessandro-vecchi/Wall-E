import cv2
import time
import numpy as np
import utils

def getLaneCurve(img, display = 2):
    streetEnded = False
    imgCopy = img.copy()
    imgResult = img.copy()

    imgThres = utils.thresholding(img)

    hT, wT, c = img.shape
    #points = utils.valTrackbars()
    points = np.float32([(106, 111), (480-106, 111),(24 , 223 ), (480-24, 223)])
    imgWarp = utils.warpImg(imgThres,points,wT,hT)

    imgWarpPoints = utils.drawPoints(imgCopy,points)

    if RoadEnded(imgWarp): streetEnded = True

    RoadCenter, imgHist = utils.getHistogram(imgWarp,display=True,minPer=0.5,region=0.75)

    imgCenter = 240

    dist = (RoadCenter - imgCenter)
    smoothDist = smoothed(dist)

    
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        smoothImg = imgResult.copy()
        cv2.putText(imgResult,str(dist),(wT//2-80,hT//2),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,0),3)

    if display == 2:
        cv2.putText(smoothImg,str(round(smoothDist,2)),(wT//2-80,hT//2),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,0),3)
        imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgThres, imgWarp],
                                            [imgHist,imgLaneColor,imgResult, smoothImg]))
        cv2.imshow('ImageStack',imgStacked)

    elif display == 1:
        cv2.imshow('Result',imgResult)

    return smoothDist, streetEnded


def RoadEnded(warpedImg):
    h, w = warpedImg.shape[:2]
    rowStart = int(0.5*h)
    rowEnd = int(0.7*h)
    nWhitePixelsFrame = warpedImg[rowStart:rowEnd].sum()/255
    threshold = 0.02
    # less than the 2% of the stripe must be white
    return nWhitePixelsFrame < threshold * (rowEnd-rowStart)*w


def smoothed(dist):
    normalizedDist = dist//240
    n = np.sqrt(np.log10(abs(normalizedDist)/4+1))
    return n * (dist>15) - n * (dist<15)





if __name__ == '__main__':
    cap = cv2.VideoCapture("../data/testReflex.avi")
    initalTrackbarVals = [106, 111, 24, 223]
    utils.initializeTrackbars(initalTrackbarVals)

    frameCounter=0
    while(cap.isOpened()):  
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        time.sleep(0.03)
        ret, img = cap.read()
        if ret == True:
            img = img[225:-12]
            img = cv2.resize(img,(480,240))
            curve = getLaneCurve(img,display=2)
            #cv2.imshow('Frame', img)
            if cv2.waitKey(1) == ord("q"):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
