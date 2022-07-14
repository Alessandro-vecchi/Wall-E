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

global centerList, distList, smoothDistList, curveAvgList, curveEstList, steeringList
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

# COUNT CSV files
countFolder = 0
while os.path.exists(os.path.join(myDirectory,f'log_{str(countFolder)}.csv')):
        countFolder += 1

def saveData(img,steering):
    global centerList, distList, smoothDistList, curveAvgList, curveEstList, steeringList

    RoadCenter, dist, smoothDist, curveAvg, curve = takeValues(img)
    print(type(smoothDist), type(curve))
    centerList.append(RoadCenter)
    distList.append(dist)
    smoothDistList.append(smoothDist)
    curveAvgList.append(curveAvg)
    curveEstList.append(curve)
    steeringList.append(steering)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    global centerList, distList, smoothDistList, curveAvgList, curveEstList, steeringList
    rawData = {
               "RoadCenter": centerList, 
                "Distance": distList, 
                "Motors' Power": smoothDistList,
                "Curve Average": curveAvgList,
                "Motors' Power 2" : curveEstList,
                'Steering': steeringList,
                }
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=True)
    print('Log Saved')
    print('Total Samples:', len(df))


def takeValues(img):
    global curveList
    # Thresholding
    imgThres = utils.thresholding(img)

    # Warping
    (hT, wT), points = (img.shape[:2], np.float32([(106, 111), (480-106, 111),(24 ,223), (480-24, 223)]))
    imgWarp = utils.warpImg(imgThres,points,wT,hT)

    # Finding center of the road
    RoadCenter = utils.getHistogram(imgWarp,display=False,minPer=0.5,region=4)

    imgCenter = 240
    # Distance from the center of the camera
    dist = (RoadCenter - imgCenter)
    smoothDist = Rm.smoothed(dist)

    # Estimate curve method 2
    curveAveragePoint = utils.getHistogram(imgWarp, display=False, minPer=0.9)
    curveRaw = curveAveragePoint - RoadCenter
 
    # Averaging
    curveList.append(curveRaw)
    if len(curveList)>10:
        curveList.pop(0)
    curve = int(np.mean(curveList))/100
    if curve>1: curve == 1
    if curve<-1: curve == -1
 
 
    return RoadCenter, dist, round(smoothDist, 3), curveAveragePoint, curve


if __name__ == '__main__':
    cap = cv2.VideoCapture(r"/Users/alessandrovecchi/Desktop/AI_Lab/computerVision/AI_lab_project/Cars-repo-1/Videos/percorsoCam.mp4")
    # Check if camera opened successfully

    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    for x in range(30):
        _, img = cap.read()
        if _:
            img = img[150:-12] # crop
            img = cv2.resize(img,(480, 240))
            
            saveData(img, 0.5)
            cv2.waitKey(1)
            cv2.imshow("Image", img)
        else: 
            print("Frame not captured properly")
    saveLog()
