
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


def detect_object():

    boundaries = [
        ([2,2,118], [40,40,255]) # works!
    #	([34,34,178], [0, 0, 255]),
    #	([25, 146, 190], [62, 174, 250]),
    #	([103, 86, 65], [145, 133, 128])
    ]
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        #while True:
        gr, frame = cv2.VideoCapture(0).read()
	frame = imutils.resize(frame, width = 300)
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
            pts.appendleft(center)
            for i in  xrange(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
                cv2.line(frame, pts[i-1], pts[i], (255,0,0), thickness)
            #cv2.imshow("Frame", frame)
            #print("The frame is at = {0}".format(center))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
            #   print('break the loop')
                break
        else:
            print('no contours found')
        #print('this is the frame to return')
        #print(frame)
        #print('return it')
        return frame

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result   

def recvall(sock, length):
    data  = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
	#print('data so far = {0}'.format(more))
        data += more
    return data


def get_values(message):
    return message.split(' ')

def make_message(portnumbers):
    str = ''
    for number in portnumbers:
        str += number + ' '
    return str[:-1]

def client(port):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('10.16.12.66' , port))        
    print('Client {} is connecting to server'.format(clientSocket.getsockname()))    
    while True:
        time.sleep(0.001)	
	#print('capture the next  frame')
        frame = detect_object()
    	cv2.imwrite("myimage.jpg", frame)
    	with open("myimage.jpg", "rb") as imageFile:
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
    clientSocket.close()
 

 
def server(port):
# socket initialization
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    serverSocket.bind(('0.0.0.0', port))
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
            #print('Waiting for information from client {}'.format(clientName))
            length_message = recvall(activeSocket, 16)
	    #print('the message = {0}'.format(length_message))
	    length_message = int(length_message)
	    message = recvall(activeSocket, length_message)
            
            imagetoshow = message.decode('base64')
	    nparr = np.fromstring(imagetoshow, np.uint8)
	    if nparr.size != 0:
		img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		cv2.imshow("result", img_np)
	    	cv2.waitKey(1)
        mySockets.append(activeSocket)
        if clientCount == 2:
            for sc in mySockets:
                sc.close()
            print('Ending the server now')
            break;
       # print('Active socket closed.')
    #    break;


if __name__ == '__main__':
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description = 'Spcify the  client or server')
    parser.add_argument('role', choices = choices, help = 'which role to play')
    parser.add_argument('host', help = 'The interface the server listens to;' 'the server the client sends to')
    parser.add_argument('-p', metavar = 'PORT', type = int,default =1060, help = 'The port to bind to')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)