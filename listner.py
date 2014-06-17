import logging, logging.handlers, socket
import GPIOlib as GPIO

if __name__ == '__main__':
    logHost = 'localhost'
    logPort = 'localhost'
    scratchHost = input('Please enter host IP (if using a local instance of Scratch \'localhost\'): ')
    scratchPort = 42001
    
    log = logging.getLogger('listner')
    log.addHandler(logging.FileHandler('listner.log'))
    #log.addHandler(logging.handlers.SocketHandler(logHost, logPort))
    
    if not scratchHost:
        log.critical('No host specified')
        print('No host specified')
        raise
    scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new local socket of type SOCK_STREAM
    print('Connecting...')
    log.info('Connecting...')
    try: 
        scratchSock.connect((scratchHost, scratchPort)) # connect the socket to scratch 
    except ConnectionRefusedError:
        print('Have you enabled remote connections in scratch and do you have a scratch instance running?')
        log.critical('Could Not Connect to Socket Address: %s Port: %d', scratchHost, scratchPort)
        raise
    print("Connected!")
    log.info("Connected!")
    
def broadcast(**pin):
  try:
    if pin['state']:
        GPIO.out(pin, state)
    else:
        GPIO.toggle(pin)
  except:
    log.warning('Invalid Argument Supplied - Pin: %s State: %s', pin['number'], pin['state'])
    
true = ['true', 'on', 'start']
false = ['false', 'off', 'stop']
PWM = {}

def createPWM(**pin):
	# pin['number'] == pin number
	# pin['frequency'] == pwm freq
	try:
		if pin['number'] in pwms.keys():
			PWM[pin['number']].ChangeFrequency(pin['frequency'])
			log.info()
		else:
			PWM[pin['number']] = GPIO.PWM(pin['number'], pin['frequency'])
			log.info()
	except exception:
		log.error()
			
def runPWM(**pin):
	# pin['number'] == pin number
	# pin['dutyCycle'] == pwm dc
	# pin['state'] == pwm state (on/off)
	try:
		if pin['number'] in pwms.keys():
			if pin['state'].lower() in false:
				PWM[pin['number']].stop()
				log.info()
			elif pin['state'].lower() in true:
				PWM[pin['number']].start(pin['dutyCycle'])
				log.info()
			else:
				log.warning()
		else:
			log.warning()
	except exception:
		log.error()

class cmdType():
        def __init__(self, name, argCnt, func):
          self.name = name
          self.argCnt = argCnt
          self.func = func

def spliceCmd(commandString):
  types = [
          cmdType('broadcast', 2, lambda args: broadcast(number=args[0], state=args[1])),
          cmdType('createPWM', 2, lambda args: createPWM(number=args[0], frequency=args[1])),
          cmdType('runPWM', 2, lambda args: runPWM(number=args[0], state=args[1])),
          ]
  commandList = commandString.split()
  i = 0
  while i < len(commandList):
    for type in types:
          if type.name == commandList[i]:
            args = []
            while len(args) < type.argCnt:
              i += 1
              if commandList[i] == '&&':
                while len(args) < type.argCnt:
                    args.append(None)
                break
              args.append(commandList[i])
            type.func(args)
    i += 1

if __name__ == '__main__':
    print 'Scratch Listner running.\nBroadcast commands in the form:\n\tpin<pin-number><on/off>\n\te.g pin7on'
    while True:
        m = scratchSock.recv(4096)
        print 'message ('+m+') received'
        spliceCmd(m)
