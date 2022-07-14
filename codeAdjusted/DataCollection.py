"""
- This module saves images and a log file.
- Images are saved in a folder.
- Folder should be created manually with the name "DataCollected"
- The name of the image and the steering angle is logged
in the log file.
- Call the saveData function to start.
- Call the saveLog function to end.
- If runs independent, will save ten images as a demo.
"""

import pandas as pd, numpy as np
import os, cv2
import utils, RoadModule as Rm
from datetime import datetime

global imgList, steeringList
countFolder = 0
count = 0
imgList = []
steeringList = []
distList = []
smoothDistList = []
centerList = []
curveList = []
curveAvgList = []
curveEstList = []

#GET CURRENT DIRECTORY PATH
myDirectory = os.path.join(os.getcwd(), 'DataCollected')
# print(myDirectory)

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT
while os.path.exists(os.path.join(myDirectory,f'IMG{str(countFolder)}')):
        countFolder += 1
newPath = myDirectory +"/IMG"+str(countFolder)
os.makedirs(newPath)


def saveData(img,steering):
    global imgList, centerList, distList, smoothDistList, steeringList

    RoadCenter, dist, smoothDist, curveAvg, curve = takeValues(img)
    
    centerList.append(RoadCenter)
    distList.append(dist)
    smoothDistList.append(smoothDist)
    curveAvgList.append(curveAvg)
    curveEstList.append(curve)
    steeringList.append(steering)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    global imgList, centerList, distList, smoothDistList, curveAvgList, curveEstList, steeringList
    rawData = {
               "RoadCenter": centerList, 
                "Distance": distList, 
                "Motors Power": smoothDistList,
                "Curve Average": curveAvgList,
                "Curve M2" : curveEstList,
                'Steering': steeringList,
                }
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Samples:', len(df))


def takeValues(img):
    global curveList
    # Thresholding
    imgThres = utils.thresholding(img)

    # Warping
    (hT, wT, points) = (img.shape[:2], np.float32([(106, 111), (480-106, 111),(24 ,223), (480-24, 223)]))
    imgWarp = utils.warpImg(imgThres,points,wT,hT)

    # Finding center of the road
    RoadCenter, _ = utils.getHistogram(imgWarp,display=False,minPer=0.5,region=4)

    imgCenter = 240
    # Distance from the center of the camera
    dist = (RoadCenter - imgCenter)
    smoothDist = Rm.smoothed(dist)

    # Estimate curve method 2
    curveAveragePoint, _ = utils.getHistogram(imgWarp, display=False, minPer=0.9)
    curveRaw = curveAveragePoint - RoadCenter
 
    # Averaging
    curveList.append(curveRaw)
    if len(curveList)>10:
        curveList.pop(0)
    curve = int(np.mean(curveList))
 
    return RoadCenter, dist, smoothDist, curveAveragePoint, curve


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    for x in range(10):
        _, img = cap.read()
        saveData(img, 0.5)
        cv2.waitKey(1)
        cv2.imshow("Image", img)
    saveLog()
