import cv2
import time
import numpy as np
import utils

curveList = []
avgVal = 10

def getLaneCurve(img, display = 2):
    flag = True
    imgCopy = img.copy()
    imgResult = img.copy()

    imgThres = utils.thresholding(img)

    hT, wT, c = img.shape
    #points = utils.valTrackbars()
    points = np.float32([(106, 111), (480-106, 111),(24 , 223 ), (480-24, 223)])
    imgWarp = utils.warpImg(imgThres,points,wT,hT)
    if (imgWarp[2*imgWarp.shape[0]//5:imgWarp.shape[1]//2,:].sum()//255 ) <400:
        flag = False

    imgWarpPoints = utils.drawPoints(imgCopy,points)

    midPoint, imgHist = utils.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp,display=True,minPer=0.9)
    curveRaw = curveAveragePoint - midPoint

    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = sum(curveList)//len(curveList)
    

    
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
        cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3)

    if display == 2:
        imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                            [imgHist,imgLaneColor,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt',imgResult)

    #### NORMALIZATION 
    curve = curve/100   
    if curve>1: curve ==1
    if curve<-1:curve == -1
    return curve,midPoint,flag


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
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
