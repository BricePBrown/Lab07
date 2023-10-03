import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)
#Following commands control the state of the output
#GPIO.output(pin, GPIO.HIGH)
#GPIO.output(pin, GPIO.LOW)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# get reading from adc 
# mcp.read_adc(adc_channel)

def blink_led(blinks, interval):
    toggle = False
    for _ in range(blinks * 2):  # Multiply by 2 because one ON and one OFF constitutes a single blink
        if toggle:
            GPIO.output(chan_list, GPIO.LOW)
        else:
            GPIO.output(chan_list, GPIO.HIGH)
        toggle = not toggle
        time.sleep(interval)

while True: 
  # Test 1, flicker 5 times with a 500ms interval
  blink_led(5, .5)

  # Test 2, for 5 seconds read light sensor
  LIGHT_THRESHOLD = 500
  for i in range(1,51):
    lightValue = mcp.read_adc(0)
    if lightValue < LIGHT_THRESHOLD:
      print(lightValue + " dark")
    else:
       print(lightValue + " bright")
    time.sleep(0.1)

  # Test 3, flicker 4 times with a 200ms interval
  blink_led(4, .2)

  # Test 4, for 5 seconds read sound sensor
  SOUND_THRESHOLD = 800
  tapped = False
  for i in range(1,51):
    soundValue = mcp.read_adc(0)
    print(soundValue)
    if soundValue > SOUND_THRESHOLD:
       GPIO.output(chan_list, GPIO.HIGH)
       tapped = True
    time.sleep(0.1)
    if(tapped):
      GPIO.output(chan_list, GPIO.LOW)
 