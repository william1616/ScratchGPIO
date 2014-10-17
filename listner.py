import logging, logging.handlers, socket
import GPIOlib as GPIO
from sys import argv, exit

if __name__ == '__main__':
    logHost = 'localhost'
    logPort = 'localhost'
    if len(argv) >= 2:
        scratchHost = argv[1]
    else:
      scratchHost = raw_input('Please enter host IP (if using a local instance of Scratch \'localhost\'): ')
    scratchPort = 42001
    
    log = logging.getLogger('listner')
    log.setLevel(logging.DEBUG)
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
    
true = ['true', 'on', 'start']
false = ['false', 'off', 'stop']

def setPin(**pin):
  # pin['number'] == pin number
  # pin['state'] == pin state
  try:
    pin['number'] = int(pin['number'])
    if pin['state']:
        if pin['state'].lower() in true:
          GPIO.out(pin['number'], True)
          log.info("Pin %d State set to On", pin['number'])
        elif pin['state'].lower() in false:
          GPIO.out(pin['number'], False)
          log.info("Pin %d State set to Off", pin['number'])
        else:
          raise
    else:
        GPIO.toggle(pin['number'])
        log.info("Pin %d State Toggled", pin['number'])
  except Exception, e:
    print e
    log.warning('Invalid Argument Supplied - Pin: %d State: %s', pin['number'], pin['state'])
    
PWMList = {}

def setPWM(**pin):
  # pin['number'] == pin number
  # pin['state'] == pin state
  # pin['dutyCycle'] == pin dc
  try:
    pin['number'] = int(pin['number'])
    if pin['number'] not in PWMList:
      PWMList[pin['number']] = GPIO.PWM(pin['number'], 60)
      log.info('PWM for Pin: %d Created', pin['number'])
    if pin['state'].lower() in true:
      PWMList[pin['number']].start(int(pin['dutyCycle']))
      log.info('Set Pin: %d DutyCycle: %s', pin['number'], pin['dutyCycle'])
    elif pin['state'].lower() in false:
      PWMList[pin['number']].stop()
      del PWMList[pin['number']]
      log.info('PWM for Pin: %d Removed', pin['number'])
    else:
      raise
  except Exception, e:
    print e
    log.warning('Invalid Argument Supplied - Pin: %d State: %s DutyCycle: %s', pin['number'], pin['state'], pin['dutyCycle'])
    
class cmdType():
        def __init__(self, name, argCnt, func):
          self.name = name
          self.argCnt = argCnt
          self.func = func

def spliceCmd(commandString):
  types = [
          cmdType('setPin', 2, lambda args: setPin(number=args[0], state=args[1])),
          cmdType('setPWM', 3, lambda args: setPWM(number=args[0], state=args[1], dutyCycle=args[2])),
          ]
  commandString = commandString[commandString.index("\"")+1:commandString.rindex("\"")]
  commandList = commandString.split()
  log.debug('Command %s Received', str(commandList))
  i = 0
  while i < len(commandList):
    for type in types:
          if type.name == commandList[i]:
            args = []
            while len(args) < type.argCnt:
              i += 1
              if len(commandList) <= i or commandList[i] == '&&':
                while len(args) < type.argCnt:
                    args.append(None)
                break
              args.append(commandList[i])
            type.func(args)
            break
    i += 1

if __name__ == '__main__':
    print 'Scratch Listner running.\nBroadcast commands in the form:\n\tsetPin <pin-number> <on/off>\n\te.g setPin 7 on'
    while True:
      try:
        m = scratchSock.recv(4096)
        print 'message ('+str(m)+') received'
        spliceCmd(m)
      except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
