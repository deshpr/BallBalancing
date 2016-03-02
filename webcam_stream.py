import socket, sys, argparse
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1' , port))  
while True:
    word = "This is a message"
