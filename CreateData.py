import cv2
import os
import time

myPath = 'data/images'
cameraNo = 1 
cameraBrightness = 190
moduleVal = 10 # save every 10 frames to avoid repetition
minBlur = 500 # threshold for blurriness: if too blurry, don't save it -> smaller value means more blurriness
grayImage = False # save image colored or grayscale
saveData = True # save data flag
showImage = True # display image flag
imgW = 180
imgH = 120

global countFolder
cap = cv2.VideoCapture(cameraNo)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, cameraBrightness)

count = 0
countSave = 0

def saveDataFunc():
    global countFolder
    countFolder = 0
    while os.path.exist(myPath+str(countFolder)):
        countFolder += 1
    os.makedirs(myPath + str(countFolder))

if saveData: saveDataFunc()

while True:

    success, img = cap.read()
    img = cv2.resize(img, (imgW, imgH))
    if grayImage: img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if saveData:
        blur = cv2.Laplacian(img, cv2.cv_64F).var()
        if count % moduleVal == 0 and blur > minBlur:
            nowTime = time.time()
            cv2.imwrite(myPath + str(countFolder) + 
                '/' + str(countSave) + " " + str(int(blur)) + " " + str(nowTime) + ".png", img)
            countSave += 1
        count += 1

    if showImage:
        cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()