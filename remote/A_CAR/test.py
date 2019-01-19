import time
import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
p = GPIO.PWM(5, 50)  # GPIO pin=18 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101):
            p.ChangeDutyCycle(int(random.random() * 100))
            time.sleep(1)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
