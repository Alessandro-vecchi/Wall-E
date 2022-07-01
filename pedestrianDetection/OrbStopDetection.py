import cv2
 
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = False)
dic = {0:'SEGNALE DI STOP'}
img2 = cv2.imread('stop.png')
orb = cv2.ORB_create()
kpts2, des2 = orb.detectAndCompute(img2,None)
vid = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
 
while(True):
    # Capture the video frame by frame
    success, img1 = vid.read()
    # matching keypoints of al the cover with the video frames
    kpts1, des1 = orb.detectAndCompute(img1, None)
    matches12 = matcher.knnMatch(des1, des2, k=2)
    #ratio test: the probability that a match is correct is determined by:
    # 1. computing the ratio of the distance from the closest neighbor to the second closest neighbor
    good_matches = []
    good_matches.append([m for m,n in matches12 if m.distance < 0.82 * n.distance])
    #select the class/book with more matches
    best = sorted(good_matches,key=len)[-1]  #maybe put reverse = True and get [0]
    #setting a treshold, if the good matches are greater than it, print the class
    if len(best) > 10:
       cv2.putText(img1,dic[good_matches.index(best)], (50,50), font,1,(0, 255, 255), 2, cv2.LINE_4)
    # Display the resulting frame
    cv2.imshow('frame', img1)
    # the 'q' button is set as the
    # quitting button you may use any
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
