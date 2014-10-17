import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
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
	
def out(pin, state):
  try:
    GPIO.output(pin, state)
  except RuntimeError:
    setOut(pin)
    GPIO.output(pin, state)

def cleanup():
  GPIO.cleanup()

class PWM(GPIO.PWM):
  def __init__(self, pin, freq):
    try:
      GPIO.PWM.__init__(self, pin, freq)
    except RuntimeError:
      setOut(pin)
      GPIO.PWM.__init__(self, pin, freq)
