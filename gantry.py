#!/usr/bin/env python3
import os
import sys
import time
import serial

# Determine OS
if sys.platform.startswith("linux"):
    system = 'linux'
elif sys.platform == "darwin":
    system = 'macos'
elif sys.platform == "win32":
    system = 'windows'


class Gantry(object):
    def __init__(self, serialString = ''):
        """
        Runs once when object is initialised
        """
        self.delay = 0.01
        self.exiting = 0
        MICROSTEPPING = 16
        STEPS_PER_REV = 200
        PULLEY_TEETH_NO = 20
        PULLEY_BELT_PITCH = 2
        PINION_CURCUMFERENCE = 43.5299
        self.STEPS_PER_MM_XY = (STEPS_PER_REV * MICROSTEPPING) / (PULLEY_TEETH_NO * PULLEY_BELT_PITCH)
        self.STEPS_PER_MM_Z = (STEPS_PER_REV * MICROSTEPPING) / PINION_CURCUMFERENCE
        self.serial_string = serialString
        if self.serial_string == '':
            print('Please pass a serial string when creating gantry object')
            print('EXITING')
            sys.exit()
        else:
            print('Connecting: ' + self.serial_string)
            self.s = serial.Serial(self.serial_string, 115200)


    def handler(self, signum, frame):  # pylint: disable=W0613
        """
        This is the handler for SIGINT events sent by the user pressing ctrl-c.
        """
        print('')
        print("Ctrl-c was pressed. Exiting...")
        self.exiting = 1
        sys.exit()



    def move(self, target_coordinate, speed):
        """
        This function is responsible for driving the gantry to the desired position
        and stalling the code function until that position is reached.
        """
        sleep = 0.01
        next_gcode_line = f'G1 X{target_coordinate[0]} Y{target_coordinate[1]} Z{target_coordinate[2]} F{speed}'
        print('sending: ' + next_gcode_line)
        self.s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        grbl_out = self.s.readline().strip().decode()
        print(f'message recieved = {grbl_out}')
        if grbl_out == 'ok':
            print('moving')
            pass
        else:
            print(' : ' + grbl_out)
        time.sleep(sleep)
        next_gcode_line = 'G4 P0'
        self.s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        print('waiting for completion')
        grbl_out = self.s.readline().strip().decode()
        if grbl_out == 'ok':
            print('Done :)')
            pass
        else:
            print('ERROR!')
            print(' : ' + grbl_out)
        # if exiting==0:
        #     break
        time.sleep(sleep)


    def homex(self):
        """
        This function is responsible for driving the gantry to the desired position
        and stalling the code function until that position is reached.
        """
        sleep = 0.01
        next_gcode_line = f'G28 X'
        print('sending: ' + next_gcode_line)
        self.s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        grbl_out = self.s.readline().strip().decode()
        print(f'message recieved = {grbl_out}')
        if grbl_out == 'ok':
            print('moving')
            pass
        else:
            print(' : ' + grbl_out)
        time.sleep(sleep)
        next_gcode_line = 'G4 P0'
        self.s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        print('waiting for completion')
        grbl_out = self.s.readline().strip().decode()
        if grbl_out == 'ok':
            print('Done :)')
            pass
        else:
            print('ERROR!')
            print(' : ' + grbl_out)
        # if exiting==0:
        #     break
        time.sleep(sleep)


if __name__ == '__main__':
    print('Please do not run this code directly. See example-move.py')
