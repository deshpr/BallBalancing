# define the list of acceptable colors


import socket, sys, argparse
import time
import base64
import cv2
from PIL import Image
import threading
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
flat_a = 0
flat_b = 0
flat_c = 0
flat_d = 0

a = flat_a
b = flat_b
c = flat_c
d = flat_d

One_Servo = Servo.Servo('PWM 3')
One_Servo.attach(3)
One_Servo.writeMicroseconds(100)
One_Servo.write(a)

Two_Servo = Servo.Servo('PWM 5')
Two_Servo.attach(5)
Two_Servo.writeMicroseconds(100)
Two_Servo.write(b)

Three_Servo = Servo.Servo('PWM 6')
Three_Servo.attach(6)
Three_Servo.writeMicroseconds(100)
Three_Servo.write(c)

Four_Servo = Servo.Servo('PWM 9')
Four_Servo.attach(9)
Four_Servo.writeMicroseconds(100)
Four_Servo.write(d)



# values that bring the platform to steady state.
def balancedState():
	global a, b, c, d
	print('goinf to baalanced strate')
	a = flat_a
	b = flat_b
	c = flat_c
	d = flat_d
	MoveServos()

def MoveServos():
	global a, b, c, d
	One_Servo.write(a)
	Two_Servo.write(b)
	Three_Servo.write(c)
	Four_Servo.write(d)
	

def square(n):
    return n * n

	
def convert_cm_to_pixels(cm_value):
    #print('pixel value = {0}'.format((cm_value*74.202)/18))
    return (cm_value*74.202)/(18)*1.5
	
def convert_pixels_to_centimeters(pixel_value):
    return ((pixel_value * 18)/74.202)	# callibrated.

def convert_point_to_cm(point_one):
    return (convert_pixels_to_centimeters(point_one[0]), convert_pixels_to_centimeters(point_one[1]))

def calculate_distance(point_one, point_two):
    return np.sqrt(square(point_one[0] - point_two[0]) + square(point_one[1] - point_two[1]))

def get_average_center(center_list):
    x_average = 0
    y_average = 0
    for i in xrange(1, len(center_list)):
	x_average += center_list[i][0]
	y_average += center_list[i][1]
    count = len(center_list)
    return (x_average/count, y_average/count)

# define the list of acceptable colors

pts = deque(maxlen = 1000)
center_pts = deque(maxlen = 1000)

def detect_object(frame):
    k =0
    last_center = None
    platform_center = None
    boundaries = [
#	([167,123,6], [195, 167, 49]), # the center. ( 206D)
	#([148, 133, 61], [158, 135, 73]), #  platform center ( 206H)
#	([164,150,101], [166,157,107]),# platform center (battery got low)
#		([161, 130, 51], [174, 143, 71]), # center
		#([156,125,64], [157,128,83]),# center
#([63, 29, 23], [77,33,32]),
	#	 ([122, 84, 30], [124, 101, 45]),
#		([118, 2, 2], [255, 40, 40]), #blue center
#([2,2,118], [123,168,255])
        ([2,2,118], [40,40,255]) # works! - red
    ]
    
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            #print('multiple contours found')
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            except ZeroDivisionError:
                continue;   # leave this center
            # only proceed if the radius meets a minimum size
            if radius > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
		cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
		if k == 1: #  ball
			#print('The center = {0}'.format(center))
    #            cv2.imwrite("result.jpg", frame)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		if k == 1:
			pts.appendleft(center)
		else:
			center_pts.appendleft(center)		
			#print('append  to  center list')         
		k = k + 1
        if center_pts!=None and len(center_pts)>0:
		last_center  = center_pts[len(center_pts) - 1]
	else:
		last_center = None
	"""
	for i in  xrange(1, len(center_pts)):
		if center_pts[i - 1] is None or center_pts[i] is None:
			continue
		last_center = center_pts[i]
		thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
		cv2.line(frame, center_pts[i-1], center_pts[i], (0,255,0), thickness)
	"""
	platform_center = last_center
	if last_center!=None:
		cv2.circle(frame, platform_center, 5, (0, 255,0), 3)
    if center!=None and last_center!=None:
	    	cv2.line(frame, platform_center, center, (255,0,0), 5)
    return (frame, platform_center, center)

def recvsize(sock):
    data = b''
    while '.' not in data:
	more = sock.recv(1);
	#print('getting size char = {0}'.format(more))
	data += more
    return data

# only for intial call


def Move_Servos(a1, a2, a3, a4):
	global a, b, c, d
	#print('parameterized move servos, a = {0}, b = {1},c = {2}, d = {3}'.format(a1,a2,a3,a4))
	if a1!=a: # write only if the angle is different
		One_Servo.write(a)
		a = a1
	if a2!=b:
		Two_Servo.write(b)
		b = a2
	if a3!=c:
		Three_Servo.write(c)
		c = a3
	if a4!=d:
		Four_Servo.write(d)
		d = a4

	
		
		
# change the values based on which servo to rotate
def determine_quadrant(platform_center, object_center):
    if platform_center == None or object_center == None:
	return -1
    if object_center[0] > platform_center[0] and object_center[1] < platform_center[1]:
	#print('At quadrant one')
	return 1
    if object_center[0] < platform_center[0] and object_center[1] < platform_center[1]:
	#print('At quadrant two')
	return 2
    if object_center[0] < platform_center[0] and object_center[1] > platform_center[1]:
	#print('At quadrant three') # one 2 id the camera is positioned to the right
	return 3
    if object_center[0] > platform_center[0] and object_center[1] > platform_center[1]:
	#print('At quadrant four') # or one if  if the camera is positioned on the right
	return 4

# change the values based on which servo to rotate
def determine_quadrant(platform_center, object_center):
    if platform_center == None or object_center == None:
	return -1
    if object_center[0] > platform_center[0] and object_center[1] < platform_center[1]:
	#print('At quadrant one')
	return 1
    if object_center[0] < platform_center[0] and object_center[1] < platform_center[1]:
	#print('At quadrant two')
	return 2
    if object_center[0] < platform_center[0] and object_center[1] > platform_center[1]:
	#print('At quadrant three') # one 2 id the camera is positioned to the right
	return 3
    if object_center[0] > platform_center[0] and object_center[1] > platform_center[1]:
	#print('At quadrant four') # or one if  if the camera is positioned on the right
	return 4


def get_rotation_angle_servo(servo_number, distance):
	#print('reset values are: {0}, {1}, {2}, {3}'.format(flat_a, flat_b, flat_c, flat_d))
	if servo_number == 1: 	
		#print('result  for servo 2= {0}'.format((distance/19.625)*(170  - flat_a) + flat_a))
		return  ((80-flat_a) + flat_a)
	elif servo_number == 2:
		#print('result  for servo 2= {0}'.format((distance/19.625)*(170  - flat_b) + flat_b))
		return  ((70 - flat_b) + flat_b)
	elif servo_number == 3:
		#print('result  for servo 3= {0}'.format((distance/19.625)*(170  - flat_c) + flat_c))
		return ((120 - flat_c) + flat_c)
	elif servo_number == 4:
		#print('result  for servo 4= {0}'.format((distance/19.625)*(170  - flat_d) + flat_d))
		return ((140 - flat_d) + flat_d)


# point: the location of the ball
# In each case, find the coordinate of the  servos ( or mid-points of the edges) 
# of the platform, and subtract with the position of the ball to get the  distance
# from the servos - no need of trig here.


class MyThread(threading.Thread):
	
	x_distance = 0
	y_distance = 0
		
		
	def __init__(self, name, x_distance,  y_distance):
		super(MyThread, self).__init__()
		#print("called constructor of Super class")
		self.x_distance = x_distance
		self.y_distance = y_distance
				
		
	def run(self):
		print("Rotate servo")
	#	print("{0} has started!".format(self.getName()))
		#print("Rotate servo {0} with angle = {1}".format(self.y_distance, self.x_distance))
		(a,b,c,d) = set_servo_angles(self.x_distance, self.y_distance)
		Move_Servos(a,b,c,d)
	#	print("{0} has finished!".format(self.getName()))


def set_servo_angles(x_distance, y_distance):
	a = 0
	b = 0
	c = 0
	d = 0
	boundary = 1
	negboundary= -1*boundary
	#print('set the servo angles')
	if x_distance > boundary: #if x is more than 3cm right
	#	print('rotate servo 2')
		c = flat_c
		a = get_rotation_angle_servo(1, x_distance)
	elif x_distance < negboundary:
	#	print('rotate servo 4')
		c = get_rotation_angle_servo(3, -1*x_distance)
		a = flat_a
	else:
		a = flat_a
		c = flat_c
	if y_distance > boundary:
	#	print('rotate servo 3')
		b = get_rotation_angle_servo(2, y_distance) # positive
		d = flat_d
	elif y_distance < negboundary:
		#print('rotate servo 4')
		d = get_rotation_angle_servo(4, -1*y_distance)
		b = flat_b
	else:
		b = flat_b
		d = flat_d	
	return (a,b,c,d)


def recvall(sock, length):
    data  = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
	#print('data so far = {0}'.format(more))
        data += more
    return data


class ClientThread(threading.Thread):
	clientSocket  = None
	def __init__(self,name, clientSocket):
		super(ClientThread, self).__init__()
		self.clientSocket = clientSocket
		
	def run(self):
		send_image(self.clientSocket)

	
def send_image(clientSocket, frame):
	cv2.imwrite("platformImage.jpg", frame)
	with open("platformImage.jpg", "rb") as imageFile:
		str_result = base64.b64encode(imageFile.read())
		word = str_result
		length_message = len(word)
		str_equiv = str(length_message)
		length_number = len(str_equiv)
		to_send_length = " " * (16 - length_number)
		to_send_length = to_send_length + str(length_message)
		#print('sending the string of length = {0}'.format(to_send_length))
		#print('the length of the message is = {0}'.format(len(word)))
		#print('sending the message')
		clientSocket.sendall(to_send_length + word)
		#print('sent the message')

def get_frame_size(frame):
	return (np.size(frame,1), np.size(frame, 0))


def set_connection():
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(('10.16.12.66' , 1060))        
	print('Client {} is connecting to server'.format(clientSocket.getsockname()))
	return clientSocket
	
frame = []
def main():
	global frame
	global a, b, c, d
	bytes_data = ''
	camera = cv2.VideoCapture(0)
#	clientSocket = set_connection()
#	clientThread = ClientThread(name="ClientThread", clientSocket = clientSocket)
	while True:
		try:
#			time.sleep(0.2)
			cv2.waitKey(200)
			_, nparr = camera.read()			
			_, nparr = camera.read()
			_, nparr = camera.read()
			_, nparr = camera.read()
			_, nparr = camera.read()
			#counter = counter + 1
			#img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			frame = imutils.resize(nparr, width = 300)
			(frame, platform_center, object_center)= detect_object(frame)			
			#clientThread.start()
			#print('Platform center = {0}, Object center = {1}'.format(platform_center, object_center))
			#quadrant  = determine_quadrant(platform_center, object_center)
			#print('The object lies in quadrant = {0}'.format(quadrant))
			# hack for now.
#			if platform_center == None and object_center!=None:
			picture_size = ()
			picture_size = get_frame_size(frame)
			platform_center= (picture_size[0]/2+30, picture_size[1]/2+20)
			cv2.circle(frame, platform_center, int(convert_cm_to_pixels(1)), (0,255,0), 3)
			#send_image(clientSocket, frame)
		#print('The platform center = {0}'.format(platform_center))
			if platform_center!=None and object_center!=None:	
				print('found the ball on the platform')
				platform_cm = convert_point_to_cm(platform_center)
				object_cm = convert_point_to_cm(object_center)
				#distance_cm = calculate_distance(platform_cm, object_cm)
				#print("coordinates, platform_center  = {0}, object center = {1}".format(platform_center, object_center))
				#print('platform center = {0}, object center = {1}'.format(platform_cm, object_cm))
				#print('The distance(cm) = {0}'.format(distance_cm))
				#print("coordinate one ={0}, and coordinate two = {1}".format(object_cm[0]-platform_cm[0],object_cm[1]-platform_cm[1]))
				#t = MyThread(name = "Thread - {0}".format("Calc and run servos"), x_distance=object_cm[0]-platform_cm[0], y_distance =object_cm[1]-platform_cm[1])
				#t.start()
				(a,b,c,d) = set_servo_angles(object_cm[0]-platform_cm[0], object_cm[1]-platform_cm[1])
				MoveServos()
				cv2.waitKey(500)
#				time.sleep(0.5)
				balancedState()
#				time.sleep(1)
				cv2.waitKey(500)
				#MoveServos()
				#cv2.imshow("result", frame)
				#cv2.waitKey(1)		
			else:
				print('Cannot find the ball')
				balancedState()	# move to original state.
		except cv2.error as e:
			print('there was an exception')
			print(e) 


balancedState()
main()
print("Ending the program")
print("Balancing the servos")
