import cv2
import numpy as np
from decimal import Decimal
import math



def histogram_equalization(frame,current_channel):

    #Initializations
    histogram_red = [0.0] *256
    pdf_red=[0.0]*256
    cdf_red=[0.0]*256
    map_red=[0.0]*256
    (height,width,channel) = frame.shape
    blank_image = np.zeros((height,width,1), np.uint8)
    # print "frame_dimension",(height,width,channel)
    total_pixel_in_image = height *width
    # print "total_pixel_in_image",total_pixel_in_image

    #Histogram of Image
    for i in range(height):
        for j in range(width):
            red_pix = frame[i,j,current_channel]
            # print red_pix
            histogram_red[red_pix] = histogram_red[red_pix]+1
    # print histogram_green

    for i in range(256):
        pdf_red[i] = (histogram_red[i] / total_pixel_in_image)
        cdf_red_temp = pdf_red[i]
        if (i == 0):
            cdf_red[0] = cdf_red_temp
        else:
            cdf_red[i] = pdf_red[i] + cdf_red[i-1]
        # print cdf_green
        current_cdf = cdf_red[i]
        map_red_temp = current_cdf * 255

        map_red_temp_string = str(map_red_temp)
        split_intenisty = map_red_temp_string.split('.')

        if (split_intenisty[1].startswith('6')):
            map_red[i] = int(map_red_temp)+1
        else:
            map_red[i] = int(map_red_temp)
    for i in range(height):
        for j in range(width):
            red_pix = frame[i,j,current_channel]
            blank_image[i,j] = map_red[red_pix]
            # print "old---->>>",frame[i,j,current_channel]
            # print "new---->>>",blank_image[i,j]

    cv2.imshow("image",blank_image)
    cv2.waitKey(0)
    return blank_image


def histogram_equalization_manager(frame):
    (height,width,channel) = frame.shape
    current_channel = 0
    blue_channel = histogram_equalization(frame,current_channel)
    current_channel = 1
    green_channel = histogram_equalization(frame,current_channel)
    current_channel = 2
    red_channel= histogram_equalization(frame,current_channel)
    image = cv2.merge((blue_channel, green_channel, red_channel))
    cv2.imshow("input",frame)
    cv2.waitKey(0)
    cv2.imshow("output",image)
    cv2.waitKey(0)


if __name__ == '__main__':
    frame = cv2.imread("test.jpg",1)
    histogram_equalization_manager(frame)
