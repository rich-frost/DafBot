from gantry import Gantry
import time
dafBot = Gantry('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303931351A071E2-if00')
# dafBot.send_command('$X', 1)
# dafBot.move_new([10,10,10], 8000)

# dafBot.send_command('G28 X', 1)
# dafBot.home_z()
# dafBot.home_x()
# dafBot.home_y()
dafBot.home_all()
# dafBot.home_z()

# dafBot.wait_until_finished()
# dafBot.send_command('G28', 1)
# dafBot.send_command('G92 X0 Y0 Z0')

# dafBot.move([0,0,0],11000)
# dafBot.move([0,0,10],11000)
# dafBot.move([0,0,0],11000)
while True:
    dafBot.move([365,220,0],11000)
    dafBot.move([365,220,-235],11000)
    dafBot.gripper_close()
    dafBot.move([365,220,0],11000)
    dafBot.move([0,0,0],11000)
    dafBot.gripper_open()
# dafBot.homex()
# dafBot.move_new([10,10,0],11000)
# while True:
#     dafBot.gripper(1000)
    # time.sleep(1)
    # dafBot.set_gripper(1000)
    # time.sleep(1)   
    # dafBot.move([0,0,0],11000)
    # dafBot.move([100,100,-100],11000)

# time.sleep(1)
# dafBot.move([730,440,-240],11000)
# dafBot.move([0,0,0],11000)
