from array import array
import socket
import time
import sys
#import GPIOlib as GPIO

if __name__ == '__main__':
    PORT = 42001
    print 'Please enter host IP (if using a local instance of Scratch \'localhost\')'
    HOST = raw_input()
    if not HOST:
        print 'No host specified\nExiting'
        sys.exit()
    print "Connecting..."
    scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new local socket of type SOCK_STREAM
    try: 
        scratchSock.connect((HOST, PORT)) # connect the socket to scratch 
    except: #add error type here
        print 'Have you enabled remote connections in scratch and do you have a scratch instance running?'
        sys.exit()
    print "Connected!" 

def sendScratchCommand(cmd):
    # split the command into its componant bits
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    scratchSock.send(a.tostring() + cmd)
        
def run_command(cmd):
    if cmd[:9] == 'broadcast':
        cmd = cmd[11:len(cmd)-1] # quotation marks and spaces take up 2 spaces before command and one after
        if cmd[:3] == 'pin':
            pin = state = ''
            for i in cmd[3:5]:
                # alternate (possibly better method): if isinstance(i, int):
                try:
                    int(i)
                    pin += i
                except ValueError:
                    break
            pin = int(pin)
            for i in cmd[3:]:
                try:
                    int(i)
                except ValueError:
                    state += i
            if state == 'on':
                state = 1
            elif state == 'off':
                state = 0
            print 'pin: '+str(pin)+' state: '+str(state)
            if isinstance(state, int):
                GPIO.out(pin, state)
        else:
            print 'Broadcast command not recognised\nTry pin<pin-number><on/off>/\e.g pin7on'

def cmdtype(msg):
    i = 0
    commands = []
    while i <= len(msg):
        #print msg[i:i + 13]
        if msg[i:i + 13] == 'sensor-update':
            #print 'its a variable change'
            commands.append(["sensor-update",i])
        #print msg[i:i + 9]
        if msg[i:i + 9] == 'broadcast':
            #print 'its a broadcast'
            commands.append(["broadcast",i])
        i += 1
    for i in commands:
        j = i[1] + len(i[0]) + 2
        while j <= len(msg):
            if msg[j] == '\"':
                break
            j += 1
        i.append(msg[i[1] + len(i[0]) + 2:j])
    for i in commands:
        print i

if __name__ == '__main__':
    print 'Scratch Listner running.\nBroadcast commands in the form:\n\tpin<pin-number><on/off>\n\te.g pin7on'
    while True:
        m = scratchSock.recv(4096)
        # the first four characters are blank so remove them before processing broadcast command
##        print 'length '+str(len(m))
##        for i in m[:4]:
##            print i
##            print 'ascii code: '+str(ord(i))
##        print m.split()
        #run_command(m[4:])
        print 'message ('+m+') received'
        cmdtype(m)
