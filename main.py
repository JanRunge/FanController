import re, os, time
import sys
from gpiozero import PWMOutputDevice, LED
from gpiozero.pins.pigpio import PiGPIOFactory
import database
import Adafruit_DHT

DB = database.connect()
# first argument is the sleeptime in seconds
if(len(sys.argv)>1):
    sleeptime = int(sys.argv[1])
else:
    sleeptime = 600

factory = PiGPIOFactory()
class Sensor:
  def __init__(self, pin):
    self.pin = pin

  def measure(self):
    self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.pin)
    return self.humidity, self.temperature
class Fan:
  def __init__(self, pwm_pin, off_pin):
    self.pwm_pin = PWMOutputDevice(pwm_pin, pin_factory=factory)
    self.off_pin = LED(off_pin)
    self.power = 1
  
  def set_power(power):
    self.power=power
    if power>0:
      self.off_pin.on()
    else:
      self.off_pin.off()
    self.pwm_pin.value=power
    
sensor_name_outter="outter"
sensor_name_lower="lower"
sensor_name_upper="upper"
sensors = {
  sensor_name_outter: Sensor(2),
  #sensor_name_lower: Sensor(2),
  sensor_name_upper: Sensor(3)
}
fans = {
  #"outter": Fan(1, 1)#,
  #"inner": Fan(1, 1)
}






def do_stuff():
  for key in sensors:
    sensors[key].measure()
    print(key)
    print(sensors[key].temperature)
  #adjust_fans()
  log_to_db()

def adjust_fans():
  fans["outter"].power=outter_fan_set_power
  difference_inside_outside = sensors[sensor_name_upper].temperature - sensors[sensor_name_outter].temperature 
  if difference_inside_outside>2:
    #adjust accordng to inside temp
    pass


    
def log_to_db():
  sqls=[]
  for key in sensors:
      sensor=sensors[key]
      temperature=sensor.temperature
      humidity=sensor.humidity
      sqls.append(f"insert into sensor_log (name, temperature, humidity) values('{key}',{temperature}, {humidity}) ")
  for key in fans:
      fan=fans[key]
      sqls.append(f"insert into fan_log (name, power) values('{key}',{fan.power}) ")
    
  for sql in sqls:
    database.execute_query(DB, sql)

def get_user_settings():
  global outter_fan_set_power
  global inner_fan_set_power
  outter_fan_set_power = 1
  inner_fan_set_power=1

# read sensor data
while True: 
    do_stuff()
    time.sleep(sleeptime)