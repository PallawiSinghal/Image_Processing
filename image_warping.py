import cv2
import imutils
import numpy as np
import os

def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # print(rect)

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

folder_path = "/folder_path/"
image_list = os.listdir(folder_path)
count  =  0

for each in image_list:
	count = count + 1
	print ("count----->",count)
	full_path = folder_path + each
	image = cv2.imread(full_path)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
	areaArray = []
  
	for c in cnts:
		# area = cv2.contourArea(c)
		# areaArray.append(area)
		# print (areaArray)
    
		peri = cv2.arcLength(c, True)
		
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	
		if len(approx) == 4:
			screenCnt = approx
			# print (screenCnt.reshape(4, 2))
			warped = four_point_transform(image, screenCnt.reshape(4, 2))
      
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.imshow("Image", image)
		cv2.imshow("warped", warped)
		cv2.waitKey(0)

