import cv2
import numpy as np
import utils

def getLaneCurve(img, display = 2):
    streetEnded = False
    imgCopy = img.copy()
    imgResult = img.copy()

    imgThres = utils.thresholding(img)

    hT, wT = img.shape[:2]
    #points = utils.valTrackbars()
    points = np.float32([(106, 111), (480-106, 111),(24 ,223), (480-24, 223)])
    imgWarp = utils.warpImg(imgThres,points,wT,hT)

    imgWarpPoints = utils.drawPoints(imgCopy,points)

    if RoadEnded(imgWarp): streetEnded = True

    RoadCenter, imgHist = utils.getHistogram(imgWarp,display=True,minPer=0.5,region=4)

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

        if dist >=0:
            cv2.putText(imgResult,str(dist)[:5],(RoadCenter-15,hT//2),cv2.FONT_HERSHEY_COMPLEX,1.5,(255, 0, 0),3)
        else:
            cv2.putText(imgResult,str(dist)[:5],(RoadCenter-40,hT//2),cv2.FONT_HERSHEY_COMPLEX,1.5,(255, 0, 0),3)

        cv2.circle(imgResult,(imgCenter,hT-10),9,(0,0,255),cv2.FILLED)
        cv2.circle(imgResult,(RoadCenter,hT-10),8,(255,200,0),3)
        cv2.line(imgResult, (imgCenter,hT-10),(RoadCenter,hT-10), (0,0,0), 4) 

    if display == 2:
        cv2.putText(smoothImg,str(round(smoothDist,2)),(wT//2-80,hT//2),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,0),3)
        imgStacked = utils.stackImages(1,([img,imgThres,imgWarpPoints],[imgWarp,imgHist,imgResult]))
        cv2.imshow('ImageStack',imgStacked)

    elif display == 1:
        cv2.imshow('Result',imgResult)

    return smoothDist, streetEnded


def RoadEnded(warpedImg,tr=0.17,a=0.5,b=1):
    h, w = warpedImg.shape[:2]
    rowStart = int(a*h)
    rowEnd = int(b*h)
    nWhitePixelsFrame = warpedImg[rowStart:rowEnd].sum()/255
    # less than the 2% of the stripe must be white
    #print(nWhitePixelsFrame)
    return nWhitePixelsFrame < tr * (rowEnd-rowStart)*w


def smoothed(dist):
    normalizedDist = dist/240
    n = np.sqrt(np.log10(abs(normalizedDist)/4+1))
    return n * (dist>15) - n * (dist<-15)


if __name__ == '__main__':
    cap = cv2.VideoCapture(r"/Users/alessandrovecchi/Desktop/AI_Lab/computerVision/AI_lab_project/Cars-repo-1/Videos/percorsoCam.mp4")

    initalTrackbarVals = [106, 111, 24, 223]
    utils.initializeTrackbars(initalTrackbarVals)

    frameCounter=0
    while(cap.isOpened()):  
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        #time.sleep(0.03)
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
