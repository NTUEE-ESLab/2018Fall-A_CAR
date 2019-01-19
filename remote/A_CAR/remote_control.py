import serial

class remote_control():
    def __init__(self):
        self.ser = serial.Serial('/dev/rfcomm0', 9600)
        self.read_enable = False
    
    def send_state_and_get_keyboard_input(self, state):
        while True:
            try:
                if self.read_enable:
                    while True: 
                        result = self.ser.read()#.decode('utf-8')
                        if result:
                            self.read_enable = False
                            return result.decode('utf-8')
                else:
                    self.ser.write(state.encode('utf-8'))
                    self.read_enable = True
            except KeyboardInterrupt:
                self.ser.close()
                break
