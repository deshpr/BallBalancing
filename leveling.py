import mraa
import Servo
import cv2
import sys
import time

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
d = int(sys.argv[4])
counter = 0

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

def balancedState():
	One_Servo.write(30)
	Two_Servo.write(50)
	Three_Servo.write(45)
	Four_Servo.write(100)

def MoveServos():
	One_Servo.write(a)
	Two_Servo.write(b)
	Three_Servo.write(c)
	Four_Servo.write(d)

while(1):
	MoveServos()