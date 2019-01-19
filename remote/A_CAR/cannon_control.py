import RPi.GPIO as GPIO
import time

SEQUENCE = [[1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]]

class cannon_control:
    def __init__(self, stepper_1_pins, stepper_2_pins, lazer_pin):        
        for pin in stepper_1_pins + stepper_2_pins + [lazer_pin]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        self.stepper_1_pins = stepper_1_pins
        self.stepper_2_pins = stepper_2_pins
        self.target_orientation = 0.
        self.target_elevation = 0.
        self.elevation = 0.

    def run():
        direction_1 = 1
        derection_2 = 1
        step_1 = 0
        step_2 = 0

        while True:
            if self.target_orientation > 180:
                direction_1 = 1
            elif self.target_orientation < 180:
                direction_1 = -1
            else:
                direction_1 = 0
            print(self.target_orientation, self.orientation)
            if self.target_elevation > self.elevation:
                direction_2 = 1
            elif self.target_elevation < self.elevation:
                direction_2 = -1
            else:
                direction_2 = 0
            
            step_1 = (step_1 + direction_1) % 8
            step_2 = (step_2 + direction_2) % 8

            self.run_one_step(self.stepper_1_pins, step_1)
            self.run_one_step(self.stepper_2_pins, step_2)
            
            self.target_orientation = (self.target_orientation -\
                self.step_size * direction_1) % 360
            
            time.sleep(0.01)

    def run_one_step(self, pins, step):
        for i in range(0, len(pins)):
            GPIO.output(pins[i], SEQUENCE[step][i])

    def fire():
        pass        
