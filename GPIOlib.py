import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pwms = []

def setOut(pin):
  GPIO.setup(pin, GPIO.OUT)

def setIn(pin):
  GPIO.setup(pin, GPIO.IN)
  
def toggle(pin):
  try:
    GPIO.output(pin, not GPIO.input(pin))
  except: # change to except <error> at later date to only catch setup errors
    setOut(pin)
    GPIO.output(pin, not GPIO.input(pin))
	
def out(pin, state):
  try:
    GPIO.output(pin, state)
  except: # change to except <error> at later date to only catch setup errors
    setOut(pin)
    GPIO.output(pin, state)

def cleanup():
  GPIO.cleanup()
  print("GPIO Clean Up Done")

def updatepwm(pin [,freq, dc, state]):
  if pin in pwms[:][1]:
    pwm = pwms[pin]
    if pwd[4] == True:
      pwm[0].start(pwm[3])
    
    

def new_pwm(pin, freq, dc, state):
  pwms.append(['pwm' + pin, pin, freq, dc, state])
  if pin in pwms[1]:
    pwms[0] = GPIO.PWM(pin, freq)
  
