import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def setOut(pin)
  GPIO.setup(pin, GPIO.OUT)

def setIn(pin)
  GPIO.setup(pin, GPIO.IN)
  
def toggle(pin)
  try:
    GPIO.output(pin, not GPIO.input(12))
  else: # change to except at later date to only catch setup errors
    setOut(pin)
    GPIO.output(pin, not GPIO.input(12))
