
import socket, sys, argparse
import time
import base64
import cv2
from PIL import Image
import numpy as np
global str

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
    clientSocket.connect(('127.0.0.1' , port))        
    print('Client {} is connecting to server'.format(clientSocket.getsockname()))
    camera = cv2.VideoCapture(0)	
    while True:
        time.sleep(0.1)	
	print('capture the next  frame')
    	_, frame = camera.read()
    	cv2.imwrite("myimage.jpg", frame)
    	with open("myimage.jpg", "rb") as imageFile:
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
            print('Waiting for information from client {}'.format(clientName))
            length_message = recvall(activeSocket, 16)
	    #print('the message = {0}'.format(length_message))
	    length_message = int(length_message)
	    message = recvall(activeSocket, length_message)
            #print('Received information from the client = {}'.format(clientName))
	    #print('the length odf the message is = {0}'.format(len(message)))
	    #print('now decoding')
            imagetoshow = message.decode('base64')
	    nparr = np.fromstring(imagetoshow, np.uint8)
	    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	    cv2.imshow("result", img_np)
	    cv2.waitKey(1)
#	    cv2.destroyAllWindows()
#	    cv2.imwrite("result.jpg", img_np)     
	    
      #      [a1, a2, a3, a4, a5] = get_values(message)
       #     message = message.decode('ascii').upper().encode('ascii')
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