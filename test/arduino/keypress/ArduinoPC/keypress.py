import msvcrt
import serial
import time
import pygame

# NOTE the user must ensure that the next line refers to the correct comm port
ser = serial.Serial('COM4' , 9600)
quit = 1
pygame.init()
keys = pygame.key.get_pressed()
while (quit != 0):
  forward = 1
  backward = 3
  left = 5
  right = 9
  movement = 0
  if keys[pygame.K_w]:
    movement = movement + forward
    print(movement)
  if keys[pygame.K_s]:
    movement = movement + backward
    print(movement)
  if keys[pygame.K_a]:
    movement = movement + left
    print(movement)
  if keys[pygame.K_d]:
    movement = movement + right
    print(movement)
  if keys[pygame.K_q]:
  	quit = 0
  if(movement == 1):ser.write('W')
  elif(movement ==3):ser.write('S')
  elif(movement == 5):ser.write('A')
  elif(movement == 9):ser.write('D')

  movement = 0
  #com = msvcrt.getch().upper()
  #ser.write(com)
  #if com == "Q":
  #	quit = 0
  #print(com)