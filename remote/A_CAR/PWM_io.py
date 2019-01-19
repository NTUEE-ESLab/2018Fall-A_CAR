import RPi.GPIO as GPIO

class PWM_output():
    def __init__(self, pin, freq, max_value):
        self.max_value = max_value
        GPIO.setup(pin, GPIO.OUT)
        self.PWM = GPIO.PWM(pin, freq)
        self.PWM.start(0)

    def write(self, value):
        if value != 0:
            PWM_value = (value + 2.5) / (self.max_value + 2) * 100
        else:
            PWM_value = (value + 1.5) / (self.max_value + 2) * 100
        # careful zero-handle
        self.PWM.ChangeDutyCycle(int(PWM_value))
