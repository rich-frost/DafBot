#!/usr/bin/env python3
import os
import sys
import time
import serial
import serial.tools.list_ports

# Determine OS
if sys.platform.startswith("linux"):
    system = 'linux'
elif sys.platform == "darwin":
    system = 'macos'
elif sys.platform == "win32":
    system = 'windows'

def FindCOMPort():
    # Assigns COM port if on a windows machine
    if sys.platform == "win32":
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in str(p):
                liststr = str(p).split("-")
                return liststr[0]
            else:
                print("Arduino Not Attached")
                quit()

    # Assigns the COM port if on a linux machine
    if sys.platform.startswith("linux"):
        return '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303931351A071E2-if00'

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
            self.s.write("\r\n\r\n".encode())
            print('Warming up - grbl')
            time.sleep(2)
            self.s.flushInput()
            
        self.send_command('$1=255')
        self.send_command('$22=1')
        self.send_command('$23=3')
        self.send_command('$24=1000')
        self.send_command('$25=5000')
        self.send_command('$27=10')
        self.send_command(f'$100={self.STEPS_PER_MM_XY}')
        self.send_command(f'$101={self.STEPS_PER_MM_XY}')
        self.send_command(f'$102={self.STEPS_PER_MM_Z}')
        self.send_command('$110=8000')
        self.send_command('$111=8000')
        self.send_command('$112=8000')
        self.send_command('$120=200')
        self.send_command('$121=200')
        self.send_command('$122=200')


    def handler(self, signum, frame):  # pylint: disable=W0613
        """
        This is the handler for SIGINT events sent by the user pressing ctrl-c.
        """
        print('')
        print("Ctrl-c was pressed. Exiting...")
        self.exiting = 1
        sys.exit()

    def move(self, target_coordinate, speed):
        self.s.flushInput()
        time.sleep(0.01)
        if target_coordinate[0] > 730:
            target_coordinate[0] = 730
        elif target_coordinate[0] < 0:
            target_coordinate[0] = 0
        if target_coordinate[1] > 440:
            target_coordinate[1] = 440
        elif target_coordinate[1] < 0:
            target_coordinate[1] = 0
        if target_coordinate[2] < -235:
            target_coordinate[2] = -235
        elif target_coordinate[0] > 0:
            target_coordinate[0] = 0
        next_gcode_line = f'G1 X{target_coordinate[0]} Y{target_coordinate[1]} Z{target_coordinate[2]} F{speed}'
        time.sleep(0.01)
        self.send_command(next_gcode_line, 1)
        time.sleep(0.01)
        self.wait_until_finished()
        time.sleep(0.01)


    def send_command(self, command = '', verbose=''):
        self.s.flushInput()
        time.sleep(0.01)
        if verbose == 1:
            print('sending: ' + command)
        self.s.write((command + '\n').encode())
        time.sleep(0.01)
        grbl_out = self.s.readline().strip().decode()
        # print(f'message recieved = {grbl_out}')
        if verbose == 1:
            print(grbl_out)
        # if grbl_out == 'ok':
        #     print('moving')
        #     pass
        # else:
        #     print(' : ' + grbl_out)
        time.sleep(0.01)


    def wait_until_finished(self):
        # print('waiting for completion')
        self.send_command('G4 P0')

    def set_current_position_as_home(self):
        self.send_command('G92 X0 Y0 Z0')

    def home_all(self):
        self.send_command('$H', 1)
        self.wait_until_finished()
        self.set_current_position_as_home()

    def home_x(self):
        self.send_command('$HX', 1)
        self.wait_until_finished()

    def home_y(self):
        self.send_command('$HY', 1)
        self.wait_until_finished()

    def home_z(self):
        self.send_command('$HZ', 1)
        self.wait_until_finished()

    def gripper_open(self):
        self.set_gripper(0)
        time.sleep(1)
    
    def gripper_close(self):
        self.set_gripper(1000) 
        time.sleep(1)   

    def set_gripper(self, closedness):
        if (closedness <= 1000) and (closedness >= 0):
            self.send_command(f'M3 S{closedness}')


if __name__ == '__main__':
    print('Please do not run this code directly. See example-move.py')
