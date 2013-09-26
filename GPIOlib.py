import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pwms = []

def setOut(pin):
  try:
    GPIO.setup(pin, GPIO.OUT)
  except:
    print 'Are you running the script as root?'
    sys.exit()

def setIn(pin):
  try:
    GPIO.setup(pin, GPIO.IN)
  except RuntimeError:
    print 'Are you running the script as root?'
    sys.exit()
  
def toggle(pin):
  try:
    GPIO.output(pin, not GPIO.input(pin))
  except RuntimeError:
    setOut(pin)
    GPIO.output(pin, not GPIO.input(pin))
  else:
    print 'Are you running the script as root?'
    sys.exit()
	
def out(pin, state):
  try:
    GPIO.output(pin, state)
  except RuntimeError:
    setOut(pin)
    GPIO.output(pin, state)
  else:
    print 'Are you running the script as root?'
    sys.exit()

def cleanup():
  GPIO.cleanup()

def updatepwm(pin, freq, dc, state):
  change = [pin, freq, dc, state]
  for i in pwms[:]:
    if i[0] == pin:
      j = 0
      while j < len(change[:]):
        i[j] = change[j]
        j += 1
      i[4].ChangeFrequency(i[1])
      i[4].ChangeDutyCycle(i[2])
      if i[3] == True:
        i[4].start(i[2])
      elif i[3] == False:
        i[4].stop()      

def new_pwm(pin, freq, dc, state):
    for i in pwms[:]:
      if i[0] == pin:
        break
    setOut(pin)
    pwms.append([pin, freq, dc, state, GPIO.PWM(pin, freq)])
    updatepwm(pin, freq, dc, state)
