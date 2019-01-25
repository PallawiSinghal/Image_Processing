
import cv2
import numpy as np
import os
from PIL import Image
import pytesseract


def bill_crop(image_path):
	
	img = cv2.imread(image_path)
	height,width,channel = img.shape
	grayscaled = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval, threshold = cv2.threshold(grayscaled, 150, 255, cv2.THRESH_BINARY)

	expected_sum_to_cut = 255 * width

	height_list = []
	cv2.imshow("threshold",threshold)

	for h in range(0,height):
		row_buffer = threshold[h, 0:width]
		calculated_sum = sum(row_buffer)
		if expected_sum_to_cut == calculated_sum:
			height_list.append(h)


	len_height_list = len(height_list)

	for l in range(0,len_height_list-1):
		sub = height_list[l+1] - height_list[l]
		if (sub > 1):
			check_1 = height_list[l] - 2
			check_2 = height_list[l+1] + 2
			# cropped_image = img[height_list[l]:height_list[l+1],0:width]
			cropped_image = img[check_1:check_2,0:width]
			output_text = pytesseract.image_to_string(cropped_image, config='--psm 6 --oem 1')
			print (output_text)
			cv2.imshow("cropped_image",cropped_image)
			cv2.waitKey(0)


if __name__ == '__main__':
	switch_crop("/21.png")#recipts,bill image
