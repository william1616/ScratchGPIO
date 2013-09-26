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

def updatepwm(pin, freq, dc, state):
  #pwms[][0, 1, 2, 3, 4]
  #pwms[][<pin>, <freq>, <dc>, <state>, <object>]
  change = [pin, freq, dc, state]
  for i in pwms[:]:
    if i[0] == pin:
      for j in len(change[:]):
        #if i[j-1] != change[j-1]:
        i[j-1] = change[j-1]
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
    pwms.append([pin, freq, dc, state, GPIO.PWM(pin, freq)])
    #pwms[len(pwms[:])-1][0]
    updatepwm(pin)
  
if __name__ == '__main__':
  new_pwm(7, 50, 50, True)
