#!/usr/bin/env python3
import random
import signal
import time

import serial
from serial.tools import list_ports

port = list(list_ports.comports())
serstring = ''
for p in port:
    if '/dev/cu.usbmodem' in p.device:
        serstring = p.device
        break
    else:
        print('Skipping: ' + p.device)
if serstring == '':
    print('No valid serial devices found')
    print('EXITING')
    quit()
else:
    print('Connecting: ' + serstring)
    s = serial.Serial(serstring, 115200)

# Wake up grbl
s.write("\r\n\r\n".encode())
print('Warming up')
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
limits = [[0, 385], [0, 400]]
coords = [[385, 0],
          [385, 400],
          [0, 400],
          [0, 0],
          [50, 0],
          [50, 50],
          [0, 50],
          [0, 0]]
x = 0
y = 0

exiting = 0


def handler(signum, frame):
    global exiting
    print('')
    # print('exiting now')
    exiting = 1


signal.signal(signal.SIGINT, handler)


def move(coord, speed):
    x = coord[0]
    y = coord[1]
    sleep = 0.01
    l = 'G1 X{:<3} Y{:<3} F{}'.format(x, y, speed)
    print('sending: ' + l)
    s.write((l + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        # print('moving')
        pass
    else:
        print(' : ' + grbl_out)
    time.sleep(sleep)
    l = 'G4 P0'
    s.write((l + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        # print('Done :)')
        pass
    else:
        print('ERROR!')
        print(' : ' + grbl_out)
    time.sleep(sleep)


while(exiting == 0):
    # for coord in coords:
    #     move(coord, 10000)

    coord = [random.randint(0, limits[0][1]), random.randint(0, limits[1][1])]
    move(coord, 10000)
    # time.sleep(2)
print('homing before quiting!')
move([0, 0], 5000)
print('closing serial')
s.close()
