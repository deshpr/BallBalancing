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
 
def recvsize(sock):
    data = b''
    while "." not in data:
	more = sock.recv(1);
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
	bytes_data+=activeSocket.recv(1024)
    	a = bytes_data.find('\xff\xd8')
   	b = bytes_data.find('\xff\xd9')
    	if a!=-1 and b!=-1:
        	jpg = bytes_data[a:b+2]
        	bytes= bytes_data[b+2:]
        	i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        	cv2.imshow(hoststr,i)
        	if cv2.waitKey(1) ==27:
            		exit(0)
