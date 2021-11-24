import re, os, time
import sys
from gpiozero import PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import database

DB = database.connect()
# first argument is the sleeptime in seconds
if(len(sys.argv)>1):
    sleeptime = int(sys.argv[1])
else:
    sleeptime = 600

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
  except (IOError) as e:
    print (time.strftime("%x %X"), "Error reading", path, ": ", e)
  return value


def do_stuff():
    current_temp = float(read_sensor())
    if current_temp == "U":
      return
    print(current_temp)
    

    log_to_db(current_temp, 0.5)
    
def log_to_db(temp, power):
    temp_insert =f"""
    insert into temperature_log (temperature) values({temp})
    """
    fan_insert =f"""
    insert into fan_log (power) values({power})
    """

    database.execute_query(DB, fan_insert)
    database.execute_query(DB, temp_insert)
# read sensor data
while True: 
    do_stuff()
    time.sleep(sleeptime)