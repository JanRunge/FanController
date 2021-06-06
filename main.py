import re, os, time

from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory

pin_fan_out = 21
fan_out = PWMLED(pin_fan_out) 


# function: read and parse sensor data file
def read_sensor():
  path = "/sys/bus/w1/devices/28-021600b914ff/w1_slave"
  value = "U"
  try:
    f = open(path, "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(float(m.group(2)) / 1000.0)
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value


def do_stuff():
    
    current_temp = read_sensor()
    print(current_temp)
    if(current_temp>28.0):
        fan_out.value= 1
    else:
        fan_out.value= 0.1

# read sensor data
while True: 
    do_stuff()
    time.sleep(1)
