import cv2, numpy as np

img1 = cv2.imread('stop.png')
img2 = cv2.imread('stop2.png')

orb = cv2.ORB_create()

kpts1, descr1 = orb.detectAndCompute(img1, None)
kpts2, descr2 = orb.detectAndCompute(img2, None)

## knn matcher
bfm = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=False)
matches = bfm.knnMatch(descr1, descr2, k=2)

# ratio test: the probability that a test is correct is determined 
# by computing the distance from the closest neighbour to the second closest neighbour
good_matches = []
for closest_neighbour, cn2 in matches:
    if closest_neighbour.distance < .03 * cn2.distance:
        good_matches.append(closest_neighbour)

# check if we have enough matches to compute the homography
if len(good_matches) > 4:
    # queryIdx is the index inside a match of a keypoint of the first image
    src_points = np.float32([kpts1[closest_neighbour.queryIdx].pt for closest_neighbour in good_matches])
    dst_points = np.float32([kpts2[closest_neighbour.trainIdx].pt for closest_neighbour in good_matches])

    # RANSAC specifies the method with which wrong matches are discarded
    transformation_matrix, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)

    y1, x1 = img1.shape[0], img1.shape[1]
    y2, x2 = img2.shape[0], img2.shape[1]
    out_img = cv2.warpPerspective(src=img1, M=transformation_matrix, dsize=(x1+x2, y1) )
    out_img[0:y2, 0:x2] = img2.copy()

    # delete black pixels on the right
    x_crop, y_crop, z_crop = np.nonzero(out_img)
    cropped_img = out_img[np.min(x_crop):np.max(x_crop), np.min(y_crop):np.max(y_crop)]
'''  
img_matches = cv2.drawMatchesKnn(img1=img1, img2=img2, keypoints1=kpts1, keypoints2=kpts2, matches1to2=matches[:50], outImg=None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("knn matches between keypoints", img_matches)
cv2.waitKey(0)
'''
cv2.imshow("panorama", cropped_img)
cv2.waitKey(0)