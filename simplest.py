#!/usr/bin/env python3
"""
Demo gantry gcode driver code for DafBot. Can move through random positions
within the bounds or do standard test procedure.
"""
import random
import signal
import sys
import time

# import cv2
import serial
from serial.tools import list_ports


def handler(signum, frame):  # pylint: disable=W0613
    """
    This is the handler for SIGINT events sent by the user pressing ctrl-c.
    """
    global EXITING  # pylint: disable=W0603
    EXITING = 1
    print('')
    print('EXITING=1')


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


# # initialise camera
# cap = cv2.VideoCapture(0)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# # print(width, height)
# RESOLUTION = 2
# if RESOLUTION == 1:
#     cap.set(3, 640)
#     cap.set(4, 240)
# if RESOLUTION == 2:
#     cap.set(3, 1280)
#     cap.set(4, 480)
# if RESOLUTION == 3:
#     cap.set(3, 2560)
#     cap.set(4, 720)
# if RESOLUTION == 4:
#     cap.set(3, 2560)
#     cap.set(4, 960)
# print('Warming up - camera')
# X = 0
# while X < 100:
#     val, img = cap.read()
#     cv2.imshow('my webcam', img)
#     if cv2.waitKey(1) == 27:
#         break  # esc to quit
#     X = X + 1


# initialise machine perameters
MACHINE_LIMITS = [[0, 385],
                  [0, 400]]
MACHINE_DEMO = [[385, 0],
                [385, 400],
                [0, 400],
                [0, 0],
                [50, 0],
                [50, 50],
                [0, 50],
                [0, 0]]
MICROSTEPPING = 16
STEPS_PER_REV = 200
PULLEY_TEETH_NO = 20
PULLEY_BELT_PITCH = 2
STEPS_PER_MM = (STEPS_PER_REV * MICROSTEPPING) / \
    (PULLEY_TEETH_NO * PULLEY_BELT_PITCH)

# initialise grbl serial
PORTS = list(list_ports.comports())
SERIAL_STRING = ''
for p in PORTS:
    if '/dev/cu.usbmodem' not in p.device:
        # print('Skipping: ' + p.device)
        pass
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
print('Warming up - grbl')
time.sleep(2)
s.flushInput()

# initialise
EXITING = 0
signal.signal(signal.SIGINT, handler)
while EXITING == 0:
    # for coord in coords:
    #     move(coord, 10000)
    xlim = MACHINE_LIMITS[0][1]
    ylim = MACHINE_LIMITS[1][1]
    for y in range(5):
        if EXITING == 1:
            break
        for x in range(5):
            if EXITING == 1:
                break
            print(x, y)
            move([(xlim/4)*x, (ylim/5)*y], 11000)
            # val, img = cap.read()
            # cv2.imshow('my webcam', img)
            # if cv2.waitKey(1) == 27:
            #     break  # esc to quit

    # coord = [random.randint(0, MACHINE_LIMITS[0][1]),
    #          random.randint(0, MACHINE_LIMITS[1][1])]
    # move(coord, 11000)

    # val, img = cap.read()
    # val, img = cap.read()
    # val, img = cap.read()
    # val, img = cap.read()
    # val, img = cap.read()
    # val, img = cap.read()
    # # img = cv2.flip(img, -1)
    # cv2.imshow('my webcam', img)
    # if cv2.waitKey(1) == 27:
    #     break  # esc to quit
print('homing before quiting!')
move([0, 0], 5000)
print('closing serial')
s.close()
# print('closing opencv')
# cap.release()
# cv2.destroyAllWindows()
