from gantry import Gantry
import time
dafBot = Gantry('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303931351A071E2-if00')
# dafBot.send_command('$X', 1)
# dafBot.move_new([10,10,10], 8000)

# dafBot.send_command('G28 X', 1)
dafBot.home_z()
dafBot.home_x()
dafBot.home_y()
# dafBot.home_z()

# dafBot.wait_until_finished()
# dafBot.send_command('G28', 1)
dafBot.send_command('G92 X0 Y0 Z0')

# dafBot.move([0,0,0],11000)
# dafBot.move([0,0,10],11000)
# dafBot.move([0,0,0],11000)
# dafBot.move([250,0,],11000)
# dafBot.homex()
# dafBot.move_new([10,10,0],11000)
# while True:
#     dafBot.move([0,0,0],11000)
#     # time.sleep(1)
#     dafBot.move([0,0,0],11000)
#     # time.sleep(1)


# time.sleep(1)
dafBot.move([650,350,-220],11000)
dafBot.move([0,0,0],11000)
