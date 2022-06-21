#!/usr/bin/env python3
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
print('Connecting: ' + serstring)
s = serial.Serial(serstring, 115200)

# Open g-code file
f = open('demo.gcode', 'r')

# Wake up grbl
s.write("\r\n\r\n".encode())
print('Warming up')
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

coords =   [[200, 0],
            [200, 200],
            [0, 200],
            [0, 0],
            [50, 0],
            [50, 50],
            [0, 50],
            [0, 0]]
x = 0
y = 0
f = 10000


def move(coord):
    x = coord[0]
    y = coord[1]
    sleep=0.01
    l = 'G1 X{} Y{} F{}'.format(x, y, f)
    print('Sending: ' + l)
    s.write((l + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        print('moving')
    else:
        print(' : ' + grbl_out)
    time.sleep(sleep)
    l = 'G4 P0'
    s.write((l + '\n').encode())  # Send g-code block to grbl
    time.sleep(sleep)
    # Wait for grbl response with carriage return
    grbl_out = s.readline().strip().decode()
    if grbl_out == 'ok':
        print('Done :)')
    else:
        print('ERROR!')
        print(' : ' + grbl_out)
    time.sleep(sleep)


while(True):
    for coord in coords:
        move(coord)
    time.sleep(2)


# Stream g-code to grbl
# for line in f:
#     l = line.strip()  # Strip all EOL characters for consistency
#     print('Sending: ' + l)
#     s.write((l + '\n').encode())  # Send g-code block to grbl
#     grbl_out = s.readline()  # Wait for grbl response with carriage return
#     print(' : ' + grbl_out.strip().decode())

# Wait here until grbl is finished to close serial port and file.
# input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
# f.close()
s.close()
