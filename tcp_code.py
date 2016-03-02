
import socket, sys, argparse
import time
import base64
import cv2
from PIL import Image
import numpy as np


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
    clientSocket.connect(('10.16.12.66' , port))        
    print('Client {} is connecting to server'.format(clientSocket.getsockname()))
    
		
    while True:
        time.sleep(0.1)
        a1 = '12'
        a2 = '15'
        a3 = '45'
        a4 = '67'
        a5 = '89'
	camera = cv2.VideoCapture(0)
    	_, frame = camera.read()
    	cv2.imwrite("myImage.jpg", frame)
    	with open("myimage.jpg", "rb") as imageFile:
		str = base64.b64encode(imageFile.read())
		word = str
		print('the length odf the message is = {0}'.format(len(word)))
#        word = make_message([a1,a2, a3, a4, a5]) 
        #print('Client {} sends the word {}'.format(clientSocket.getsockname(), word))
	print('sending the message')
        clientSocket.sendall(word)
	print('sent the message')
        #print('Client has send the word = ' + word)
  #      reply = recvall(clientSocket, len(word))
#        print('Server responded with {}'.format(repr(reply)))
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
            message = recvall(activeSocket, 50884)
	    #message = activeSocket.recv(256 * 100)
            print('Received information from the client = {}'.format(clientName))
	    print('the length odf the message is = {0}'.format(len(message)))
	    print('now decoding')
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