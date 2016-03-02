import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--r", help  = "entyer the color")
ap.add_argument("-g", "--g", help  = "entyer the color")
ap.add_argument("-b", "--b", help  = "entyer the color")
args = vars(ap.parse_args())
red = int(args["r"])
green = int(args["g"])
blue = int(args["b"])
print("red = {0}".format(red))
print("green = {0}".format(green))
print("blue = {0}".format(blue))

color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
print hsv_color
