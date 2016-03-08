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
while True:
    print('Waiting for a new request')
    activeSocket, clientName = serverSocket.accept()
    clientCount += 1
    print('Server {} has connected to client {}'.format(activeSocket.getsockname(),activeSocket.getpeername()))
    print('The involved client is: {}'.format(clientName))
    print('Server is now reading stuff')
    while True:
    # process no more than one word.
        print('Waiting for information from client {}'.format(clientName))
	print('obtaining the size')
	size_length = recvall(activeSocket, 16)
	print('Length of image = {0}'.format(int(size_length)))
    	message = recvall(activeSocket,int(size_length))
	a = message.find('\xff\xd8')
	b = message.find('\xff\xd9')
	if a!=-1 and b!=-1:
		print('this image is clear')
		print('received the imge of specified size = {0}'.format(len(message)))
    		imagetoshow = message.decode('base64')
        	nparr = np.fromstring(imagetoshow, np.uint8)
		print('obtained the nparr')
		print('result = {0}'.format(nparr))
		with open('resulting.jpg', 'wb') as img:
			img.write(nparr)
		print('done writing the data')
	else:
		print('image not clear')
#	if nparr.size != 0:
#		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#		cv2.imwrite("result.jpg", img_np)
##	    	cv2.waitKey(0)
#	break