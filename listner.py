from array import array
import socket
import time
import sys

PORT = 42001
HOST = 'localhost'

print("Connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new local socket of type SOCK_STREAM
scratchSock.connect((HOST, PORT)) # connect the socket to scratch 
print("Connected!")

def sendScratchCommand(cmd):
	# split the command into its componant bits
	n = len(cmd)
	a = array('c')
	a.append(chr((n >> 24) & 0xFF))
	a.append(chr((n >> 16) & 0xFF))
	a.append(chr((n >>  8) & 0xFF))
	a.append(chr(n & 0xFF))
	scratchSock.send(a.tostring() + cmd)

while True:
	print scratchSock.recv(4096)
