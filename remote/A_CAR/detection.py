import time
import numpy as np
import serial

class detection:
    def __init__(self, address_1, address_2, init_state):
        self.sensor_num = 17
        self.serial_1 = serial.Serial(address_1, 9600)
        self.serial_2 = serial.Serial(address_2, 9600)
        self.state = init_state
        self.orientation = 0.
        self.elevation = 0.
        self.result = (self.state, self.orientation, self.elevation)

    def mean_of_angles(self, angles):
        angles = np.array(angles)
        x = np.mean(np.cos(angles * np.pi / 180))
        y = np.mean(np.sin(angles * np.pi / 180))
        rad = np.arctan2(y, x)
        degree = rad / np.pi * 180
        return degree if degree >= 0 else degree + 360

    def detect(self):
        while self.state == 'c':
            orientations = []
            elevations = []
            data = self.serial_1.readline().decode('utf-8').strip('\n') +\
                self.serial_2.readline().decode('utf-8;').strip('\n')
            
            for i in range(self.sensor_num):
                if i == self.sensor_num - 1 and int(data[i]):
                    # top sensor
                    orientations.append(0)
                    elevations.append(90)
                elif int(data[i]):
                    # side sensors
                    #orientations.append(360 / self.stick_num  / 2 *\
                    #    (i // 2 * 2 + 1))
                    orientations.append(360 / 8  / 2 *\
                        (i % 8 * 2 + 1))
                    elevations.append((i // 8) * 60)

            if orientations != []:
                self.orientation = self.mean_of_angles(orientations)
                self.elevation = self.mean_of_angles(elevations)
                self.state = 'd'
                self.result = self.state, self.orientation, self.elevation
            elif self.state == 'c':
                self.orientation = 0.
                self.elevation = 0
                self.state = 'c'
                self.result = self.state, self.orientation, self.elevation
            else:
                self.result = self.result

            time.sleep(0.05)

    def detect_one_time(self):
        data = self.serial_1.readline().decode('utf-8').strip('\n') +\
            self.serial_2.readline().decode('utf-8;').strip('\n')
        for i in range(self.sensor_num):
            if int(data[i]):
                orientation = 360 / 8  / 2 * (i % 8 * 2 + 1)
                elevation = (i // 8) * 60
                return orientation, elevation
        return 0., 0.
