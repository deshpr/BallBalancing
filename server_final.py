# a simple server program


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
 

# define the list of acceptable colors


pts = deque(maxlen = 1000)
center_pts = deque(maxlen = 1000)

def detect_object(frame):

    boundaries = [
	([167,123,6], [195, 167, 49]), # the center.
        ([2,2,118], [40,40,255]) # works! - red
	
    #	([34,34,178], [0, 0, 255]),
    #	([25, 146, 190], [62, 174, 250]),
    #	([103, 86, 65], [145, 133, 128])
    ]
    k = 0
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        #while True:
        #gr, frame = cv2.VideoCapture(0).read()
	#frame = imutils.resize(frame, width = 300)
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask)
    #    cv2.imshow("images", np.hstack([frame, output]))
    #    cv2.imshow("images.png", output)
    #    cv2.imwrite('blueImage.png', output)
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
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
    #            cv2.imwrite("result.jpg", frame)
            if k == 0:
		pts.appendleft(center)
	    else:
		center_pts.appendleft(center)
            for i in  xrange(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
                cv2.line(frame, pts[i-1], pts[i], (255,0,0), thickness)
            for i in  xrange(1, len(center_pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
                cv2.line(frame, pts[i-1], pts[i], (0,255,0), thickness)

            #cv2.imshow("Frame", frame)
            #print("The frame is at = {0}".format(center))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
            #   print('break the loop')
                break
        else:
            print('no contours found')
	k = k + 1
        #print('this is the frame to return')
        #print(frame)
        #print('return it')
        return frame




def recvsize(sock):
    data = b''
    while '.' not in data:
	more = sock.recv(1);
	#print('getting size char = {0}'.format(more))
	data += more
    return data


def recvall(sock, length):
    data  = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
	#print('data so far = {0}'.format(more))
        data += more
    return data


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
serverSocket.bind(('0.0.0.0', 1069))
serverSocket.listen(2) # work with only a single client.
print('Listening at ', serverSocket.getsockname())
mySockets = []
clientCount = 0;
bytes_data = ''
while True:
    print('Waiting for a new request')
    activeSocket, clientName = serverSocket.accept()
    clientCount += 1
    print('Server {} has connected to client {}'.format(activeSocket.getsockname(),activeSocket.getpeername()))
    print('The involved client is: {}'.format(clientName))
    print('Server is now reading stuff')
    while True:
            # process no more than one word.
        #print('Waiting for information from client {}'.format(clientName))
        length_message = recvsize(activeSocket)
	#print('the message = {0}'.format(length_message))
	length_message = int(length_message[:-1])
	#print('receive an image of length = {0}'.format(length_message))
	message = recvall(activeSocket, length_message)
	missing_padding = 4 - len(message) % 4
    	if missing_padding:
        	message += b'='* missing_padding
        imagetoshow = message.decode('base64')
	nparr = np.fromstring(imagetoshow, np.uint8)
	frame = []
	if nparr.size != 0:
		try:
	            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        	    frame = imutils.resize(img_np, width = 300)
            	    frame = detect_object(frame)
            	    cv2.imshow("result", frame)
                    cv2.waitKey(1)
       		except cv2.error as e:
		    print('there was an exception')
       		    print(e) 
		    
		
           #else:
         #   print('did not get a clear image yet')