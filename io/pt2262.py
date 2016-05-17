#!/usr/bin/python

import sys, getopt
import RPi.GPIO as GPIO
import time

SEND_PIN = 17

SIGNATURE = 0b0000111101010101

COMMAND = 0b11110001

DELAYSHORT = 160
DELAYLONG = 500

OVERHEAD = 0 # overhead time (in us) for calling GPIO.output and time.sleep. If 0 doesn't work, try 125

def ookPulse(on,off):
  GPIO.output(SEND_PIN,True)
  time.sleep((on-OVERHEAD)/1000000.0)
  GPIO.output(SEND_PIN,False)
  time.sleep((off-OVERHEAD)/1000000.0)

def pt2262Send(signature,command):
  for k in range(0,5):
    for i in range(0,16):
      if((signature>>(15-i)) & 0x1):
        ookPulse(DELAYLONG, DELAYSHORT)
      else:
        ookPulse(DELAYSHORT, DELAYLONG);      
    for i in range(0,8):
      if((command>>(7-i)) & 0x1):
        ookPulse(DELAYLONG, DELAYSHORT)
      else:
        ookPulse(DELAYSHORT, DELAYLONG)
    ookPulse(DELAYSHORT, DELAYLONG)
    time.sleep(.005)
#    sys.stdout.write("\n")
#    sys.stdout.flush()

def main(argv):
  opts, args = getopt.getopt(argv,"hs:c:",["command=","signature="])
  sign = SIGNATURE
  cmd = COMMAND
  for opt, arg in opts:
      if opt == '-h':
         print 'test.py -c <command(0-255)> -s <signature(0-65535)>'
         sys.exit()
      elif opt in ("-c", "--command"):
         cmd = int(arg)
      elif opt in ("-s", "--signature"):
         sign = int(arg)
  print 'Debug: command "{0:b}"'.format(cmd)
  print 'Debug: signature "{0:b}"'.format(sign)

  GPIO.setwarnings(False)
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(SEND_PIN,GPIO.OUT)
#  while True:
  pt2262Send(sign,cmd)
#  time.sleep(5)

if __name__ == "__main__":
  main(sys.argv[1:])
