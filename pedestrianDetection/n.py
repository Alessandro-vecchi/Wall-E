import cv2

img1 = cv2.imread('STOPphotos/stop2.jpg', 0)
print(img1)
cv2.imshow("STOP", img1)
cv2.waitKey(0)