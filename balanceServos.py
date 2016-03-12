# define the list of acceptable colors


import socket, sys, argparse
import time
import base64
import cv2
from PIL import Image
import imutils
import numpy as np
global str
import argparse
from collections import deque
import cv2
import mraa
import Servo
import time

locked_center = None
flat_a = 10
flat_b = 10
flat_c = 70
flat_d = 80

a = flat_a
b = flat_b
c = flat_c
d = flat_d

One_Servo = Servo.Servo('PWM 3')
One_Servo.attach(3)
One_Servo.writeMicroseconds(700)
One_Servo.write(a)

Two_Servo = Servo.Servo('PWM 5')
Two_Servo.attach(5)
Two_Servo.writeMicroseconds(700)
Two_Servo.write(b)

Three_Servo = Servo.Servo('PWM 6')
Three_Servo.attach(6)
Three_Servo.writeMicroseconds(700)
Three_Servo.write(c)

Four_Servo = Servo.Servo('PWM 9')
Four_Servo.attach(9)
Four_Servo.writeMicroseconds(700)
Four_Servo.write(d)


def MoveServos():
	global a, b, c, d
	print('a = {0}, b = {1},c = {2}, d = {3}'.format(a, b, c, d))
	One_Servo.write(a)
	Two_Servo.write(b)
	Three_Servo.write(c)
	Four_Servo.write(d)


# values that bring the platform to steady state.
def balancedState():
	global a, b, c, d
	a = flat_a
	b = flat_b
	c = flat_c
	d = flat_d
	MoveServos()

count = 0
balancedState()
print("balancing servos")
while count < 1000:
	count = count + 10
print("Done balancing")
