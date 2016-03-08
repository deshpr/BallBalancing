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
            # process no more than one word.
        print('Waiting for information from client {}'.format(clientName))
        length_message = recvsize(activeSocket)
	print('the message = {0}'.format(length_message))
	length_message = int(length_message[:-1])
	print('receive an image of length = {0}'.format(length_message))
	message = recvall(activeSocket, length_message)
	missing_padding = 4 - len(message) % 4
    	if missing_padding:
        	message += b'='* missing_padding
        imagetoshow = message.decode('base64')
	nparr = np.fromstring(imagetoshow, np.uint8)
	frame = []
	if nparr.size != 0:
		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		frame = imutils.resize(img_np, width = 300)
		cv2.imshow("result", frame)
	    	cv2.waitKey(1)
		
           #else:
         #   print('did not get a clear image yet')