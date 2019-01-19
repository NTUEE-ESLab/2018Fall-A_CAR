import cv2
import threading
import serial
import time
import RPi.GPIO as GPIO 
from recognition import recognition
from video_serial_server import video_serial_server
from remote_control import remote_control
from detection import detection
from cannon_control import cannon_control
from PWM_io import PWM_output

PWM_freq = 50
wheel_pin = 5
stepper_1_pins = [18, 23, 24, 25]
stepper_2_pins = [4, 17, 27, 22]
lazer_pin = 21

GPIO.setmode(GPIO.BCM)
#'c': 'controlling', 'd': attacked and detecting, 'r': 'recognizing', 'a': 'firing'
state = 'c'
prev_keyboard_input = 'A'

video_capturer = cv2.VideoCapture(0)

video_sender = video_serial_server(5005)
video_sender_thread = threading.Thread(target = video_sender.run)
video_sender_thread.start()

#remote_controller = remote_control()
#wheel_controller = PWM_output(wheel_pin, PWM_freq, 16)

# persistent symbolic link for our arduino device
#detector = detection('/dev/sensor_1', '/dev/sensor_2', state)
#detector_thread = threading.Thread(target = detector.detect)
#detector_thread.start()

#cannon_controller = cannon_control(stepper_1_pins, stepper_2_pins, lazer_pin)
#cannon_controller_thread = threading.Thread(target = cannon_control)

try:
    while state == 'c':
        ret, frame = video_capturer.read()
        cv2.imshow('Video', frame)
        video_sender.data = frame[::5, ::5, 2::-1]
        
        #video_sender.data = frame[::5, ::5, ::-1]
        #state, orientation, elevation = detector.result
        #if orientation != 0.:
        #    cannon_controller.target_orientation = orientation
        #    cannon_controller.target_elevation = elevation
        # move the step motor if necessary       
        #keyboard_input = remote_controller.send_state_and_get_keyboard_input(state)
        #if keyboard_input != prev_keyboard_input:
        #    prev_keyboard_input = keyboard_input
        #    wheel_controller.write(ord(keyboard_input) - ord('A'))
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    #video_sender_thread.join()
    detector_thread.join()
    time.sleep(10)
    print('sleeping')

    count = 0
    while state == 'd':
        remote_controller.send_state_and_get_keyboard_input(state)
        orientation, detection = detector.detect_one_time()
        if orientation != 0.:
            cannon_controller.target_orientation = orientation
            cannon_controller.target_elevation = elevation
            time.sleep(10)
            state = 'r'
            break
        else:
            cannon_controller.target_orientation = 12
            time.sleep(1)
            count += 1
        if count >= 36:
            #restart
            break
         
    remote_controller.send_state_and_get_keyboard_input(state)
    recognizer = recognition(video_capturer, video_sender,\
        cannon_controller)
    recognizer.search()
    state = 'f'
    remote_controller.send_state_and_get_keyboard_input(state)

except KeyboardInterrupt:
    video_capturer.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
