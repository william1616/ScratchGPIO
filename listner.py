from array import array
import socket
import time
import sys
import GPIOlib as GPIO

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
	
def run_command(cmd)
	if cmd[:3] == 'pin':
		pin = state = ''
		for i in cmd [3:5]:
			#if isinstance(i, int):
			try:
				int(i)
				pin += i
			except ValueError:
				break
		pin = int(pin)
		for i in cmd[3:]:
			try:
				str(i)
				state += i
			except ValueError:
				pass
		if state == 'on':
			state = 1
		elif state == 'off':
			state = 0
		GPIO.out(pin, state)

while True:
	run_command(scratchSock.recv(4096))