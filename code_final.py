
from collections import deque
import numpy as np

import argparse
import imutils
import cv2

ap  = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the video file")
ap.add_argument("-b", "--buffer", type=int, default = 64, help = "max buffer suze")
args = vars(ap.parse_args())

# determined from http://www.workwithcolor.com/red-color-hue-range-01.htm
[17, 15, 100], [50, 56, 200]
redlower = (17,15,100)
redupper = (50,56,200)
#lower = np.array(redlower, dtype = "uint8")
#upper = np.array(redupper, dtype = "uint8")
pts = deque(maxlen = args["buffer"])


if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])


# returns a tuple. 
# grabbed indicates whether the frame was grabbed successfully or not
# and frame refers to the frame.
grabbed, frame = camera.read()
#frame = cv2.imread("usethis.jpg")
frame = imutils.resize(frame, width = 600)
cv2.imshow("images", frame)
cv2.waitKey(0)
# Blur the frame to reduce any sort of noise.
blurred = cv2.GaussianBlur(frame, (11,11), 0)
# now convert the color to Hue, Saturation and Value space.
# Hue - the primary color
# Saturation - the lightness, or whiteness added to the color.
# Value - how much of darkness we havE

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


# construct the mask

lower_red = np.array([169,110,150])
upper_red = np.array([174,255,200])
mask = cv2.inRange(hsv,lower_red,upper_red)
mask = cv2.erode(mask, None, iterations = 2)
mask = cv2.dilate(mask, None, iterations = 2)

result = cv2.bitwise_and(frame, frame, mask = mask)

cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.imshow("frame", frame)
cv2.waitKey(0)
cv2.imshow("res", result)
cv2.waitKey(0)
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None
if len(cnts) > 0:
    print('multiple contours found')
else:
    print('no contours found')



     
     
     



