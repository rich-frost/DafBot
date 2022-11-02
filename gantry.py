#!/usr/bin/env python3
import os
import sys
import time

# Determine OS
if sys.platform.startswith("linux"):
    system = 'linux'
elif sys.platform == "darwin":
    system = 'macos'
elif sys.platform == "win32":
    system = 'windows'


class Gantry(object):
    def __init__(self, serialString):
        """
        Runs once when object is initialised
        """
        self.delay = 0.01
        self.exiting = 0
        MICROSTEPPING = 16
        STEPS_PER_REV = 200
        PULLEY_TEETH_NO = 20
        PULLEY_BELT_PITCH = 2
        self.STEPS_PER_MM = (STEPS_PER_REV * MICROSTEPPING) / (PULLEY_TEETH_NO * PULLEY_BELT_PITCH)


    def handler(self, signum, frame):  # pylint: disable=W0613
        """
        This is the handler for SIGINT events sent by the user pressing ctrl-c.
        """
        print('')
        print("Ctrl-c was pressed. Exiting...")
        self.exiting = 1
        sys.exit()

    def move(target_coordinate, speed):
        """
        This function is responsible for driving the gantry to the desired position
        and stalling the code function until that position is reached.
        """
        next_gcode_line = f'G1 X{target_coordinate[0]} Y{target_coordinate[1]} F{speed}'
        print('sending: ' + next_gcode_line)
        s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        grbl_out = s.readline().strip().decode()
        print(f'message recieved = {grbl_out}')
        if grbl_out == 'ok':
            print('moving')
            pass
        else:
            print(' : ' + grbl_out)
        time.sleep(sleep)
        next_gcode_line = 'G4 P0'
        s.write((next_gcode_line + '\n').encode())  # Send g-code block to grbl
        time.sleep(sleep)
        # Wait for grbl response with carriage return
        print('waiting for completion')
        grbl_out = s.readline().strip().decode()
        if grbl_out == 'ok':
            print('Done :)')
            pass
        else:
            print('ERROR!')
            print(' : ' + grbl_out)
        # if exiting==0:
        #     break
        time.sleep(sleep)

    def print_output(self):
        """
        prints the output of calculation.
        """
        print(f'The output of the calculation is {self.val_c}')

    def print_forever(self):
        """
        calls print_output for all eternity
        """
        while True:
            self.print_output()
            time.sleep(0.1)


if __name__ == '__main__':
    instance = MyClass()
    instance.print_forever()
