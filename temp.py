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



# values that bring the platform to steady state.
def balancedState():
	global a, b, c, d
	a = flat_a
	b = flat_b
	c = flat_c
	d = flat_d
	MoveServos()



def square(n):
    return n * n

def convert_pixels_to_centimeters(pixel_value):
    return (pixel_value * 18)/74.202	# callibrated.

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
		 ([122, 84, 30], [124, 101, 45]),
#		([118, 2, 2], [255, 40, 40]), #blue center
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
			print('The center = {0}'.format(center))
    #            cv2.imwrite("result.jpg", frame)
	    cv2.circle(frame, center, 5, (0, 0, 255), -1)
	    print('the k = {0}'.format(k))
            if k == 1:
		pts.appendleft(center)
	    else:
		center_pts.appendleft(center)		
		print('append  to  center list')            
            #cv2.imshow("Frame", frame)
            #print("The frame is at = {0}".format(center))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
            #   print('break the loop')
                break
        else:
            print('no contours found')
	k = k + 1
    # implement the drawing
        #cv2.line(frame, pts[i-1], pts[i], (255,0,0), thickness)
    for i in  xrange(1, len(center_pts)):
		if center_pts[i - 1] is None or center_pts[i] is None:
			continue
		last_center = center_pts[i]
		thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
		cv2.line(frame, center_pts[i-1], center_pts[i], (0,255,0), thickness)
	platform_center = last_center
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


def MoveServos():
	global a, b, c, d
	print('a = {0}, b = {1},c = {2}, d = {3}'.format(a, b, c, d))
	One_Servo.write(a)
	Two_Servo.write(b)
	Three_Servo.write(c)
	Four_Servo.write(d)

		
# change the values based on which servo to rotate
def determine_quadrant(platform_center, object_center):
    if platform_center == None or object_center == None:
	return -1
    if object_center[0] > platform_center[0] and object_center[1] < platform_center[1]:
	print('At quadrant one')
	return 1
    if object_center[0] < platform_center[0] and object_center[1] < platform_center[1]:
	print('At quadrant two')
	return 2
    if object_center[0] < platform_center[0] and object_center[1] > platform_center[1]:
	print('At quadrant three') # one 2 id the camera is positioned to the right
	return 3
    if object_center[0] > platform_center[0] and object_center[1] > platform_center[1]:
	print('At quadrant four') # or one if  if the camera is positioned on the right
	return 4


def get_rotation_angle_servo(servo_number, distance):
	print('distance = {0}'.format(distance))
	print('number = {0}'.format(distance/19.75))
	if(distance>19.75):
		distance = 19.75
	
	print('reset values are: {0}, {1}, {2}, {3}'.format(flat_a, flat_b, flat_c, flat_d))
	if servo_number == 1: 	
		print('result  for servo 2= {0}'.format((distance/19.625)*(170  - flat_a) + flat_a))
		return  ((distance/19.75)*(170  - flat_a) + flat_a)
	elif servo_number == 2:
		print('result  for servo 2= {0}'.format((distance/19.625)*(170  - flat_b) + flat_b))
		return  ((distance/19.625)*(170  - flat_b) + flat_b)
	elif servo_number == 3:
		print('result  for servo 3= {0}'.format((distance/19.625)*(170  - flat_c) + flat_c))
		return ((distance/19.75)*(170  - flat_c) + flat_c)
	elif servo_number == 4:
		print('result  for servo 4= {0}'.format((distance/19.625)*(170  - flat_d) + flat_d))
		return ((distance/19.625)*(170  - flat_d) + flat_d)


# point: the location of the ball
# In each case, find the coordinate of the  servos ( or mid-points of the edges) 
# of the platform, and subtract with the position of the ball to get the  distance
# from the servos - no need of trig here.




def set_servo_angles(x_distance, y_distance):
	global a, b, c, d
	print('set the servo angles')
	if x_distance > 3: #if x is more than 3cm right
		a = flat_a
		c = get_rotation_angle_servo(2, x_distance)
	elif x_distance < -3:
		a = get_rotation_angle_servo(4, -1*x_distance)
		c = flat_c
	else:
		a = flat_a
		c = flat_c
	if y_distance > 3:
		b = get_rotation_angle_servo(3, y_distance) # positive
		d = flat_d
	elif y_distance < -3:
		d = get_rotation_angle_servo(1, -1*y_distance)
		b = flat_b
	else:
		d = flat_d
		b = flat_b	
	print('In the method, a = {0}, b = {1},c = {2}, d = {3}'.format(a, b, c, d))
	


def recvall(sock, length):
    data  = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
	#print('data so far = {0}'.format(more))
        data += more
    return data


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
		print('sending the string of length = {0}'.format(to_send_length))
		print('the length of the message is = {0}'.format(len(word)))
		print('sending the message')
		clientSocket.sendall(to_send_length + word)
		print('sent the message')

def get_frame_size(frame):
	return (np.size(frame,1), np.size(frame, 0))
		
	
def main():
	global a, b, c, d
	bytes_data = ''
	camera = cv2.VideoCapture(0)
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(('10.16.12.66' , 1060))        
	print('Client {} is connecting to server'.format(clientSocket.getsockname()))
	while True:
		try:			
			_, nparr = camera.read()
			#img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			frame = imutils.resize(nparr, width = 300)		
			(frame, platform_center,  object_center)= detect_object(frame)
			send_image(clientSocket, frame)
			#print('Platform center = {0}, Object center = {1}'.format(platform_center, object_center))
			quadrant  = determine_quadrant(platform_center, object_center)
			#print('The object lies in quadrant = {0}'.format(quadrant))
			# hack for now.
#			if platform_center == None and object_center!=None:
			picture_size = ()
			picture_size = get_frame_size(frame)
			platform_center= (picture_size[0]/2, picture_size[1]/2)
			print('The platform center = {0}'.format(platform_center))
			if platform_center!=None and object_center!=None:				
				platform_cm = convert_point_to_cm(platform_center)
				object_cm = convert_point_to_cm(object_center)
				distance_cm = calculate_distance(platform_cm, object_cm)
				print('The distance(cm) = {0}'.format(distance_cm))
				set_servo_angles(object_cm[0]-platform_cm[0], object_cm[1]-platform_cm[1])
				MoveServos()
				#MoveServos()
				#cv2.imshow("result", frame)
				#cv2.waitKey(1)		
			else:
				balancedState()	# move to original state.
		except cv2.error as e:
			print('there was an exception')
			print(e) 


balancedState()
main()
print("Ending the program")
print("Balancing the servos")
