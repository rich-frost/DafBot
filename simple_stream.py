#!/usr/bin/env python3
"""
Demo gantry gcode driver code for DafBot. Can move through random positions
within the bounds or do standard test procedure.
"""
import random
import signal
import sys
import time

import serial
from serial.tools import list_ports

port = list(list_ports.comports())
SETSTRING = ''
for p in port:
    if '/dev/cu.usbmodem' not in p.device:
        print('Skipping: ' + p.device)
    else:
        SERIAL_STRING = p.device
        break
if SERIAL_STRING == '':
    print('No valid serial devices found')
    print('EXITING')
    sys.exit()
else:
    print('Connecting: ' + SERIAL_STRING)
    s = serial.Serial(SERIAL_STRING, 115200)
s.write("\r\n\r\n".encode())
print('Warming up')
time.sleep(2)
s.flushInput()
limits = [[0, 385], [0, 400]]
coords = [[385, 0],
          [385, 400],
          [0, 400],
          [0, 0],
          [50, 0],
          [50, 50],
          [0, 50],
          [0, 0]]
EXITING = 0
STEPS_PER_MM = (200 * 16) / (20 * 2)


def handler(signum, frame): # pylint: disable=W0613
    """
    This is the handler for SIGINT events sent by the user pressing ctrl-c.
    """
    global EXITING # pylint: disable=W0603
    EXITING = 1
    print('Kill signal recieved')


signal.signal(signal.SIGINT, handler)


def move(target_coordinate, speed):
    """
    This function is responsible for driving the gantry to the desired position
    and stalling the code function until that position is reached.
    """
    sleep = 0.01
    next_gcode_line = f'G1 X{target_coordinate[0]} Y{target_coordinate[1]} F{speed}'
    print('sending: ' + next_gcode_line)
    s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        # print('moving')
        pass
    else:
        print(' : ' + grbl_out)
    time.sleep(sleep)
    next_gcode_line = 'G4 P0'
    s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        # print('Done :)')
        pass
    else:
        print('ERROR!')
        print(' : ' + grbl_out)
    # if exiting==0:
    #     break
    time.sleep(sleep)


while EXITING == 0:
    # for coord in coords:
    #     move(coord, 10000)
    coord = [random.randint(0, limits[0][1]), random.randint(0, limits[1][1])]
    move(coord, 11000)
print('homing before quiting!')
move([0, 0], 5000)
print('closing serial')
s.close()
