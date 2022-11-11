from gantry import Gantry
from gantry import FindCOMPort as FCOM
import time
import sys

dafBot = Gantry(FCOM())
# Assigns current position as 0,0,0, make sure you move head to start position to ensure it sets home correctly. 
dafBot.send_command('$X')
dafBot.move([0,0,240],11000)
dafBot.set_current_position_as_home()

# Main Loop
while True:
    # Moves the gantry to set position
    dafBot.move([365,220,0],11000)
    dafBot.gripper_open()
    dafBot.move([365,220,-235],11000)
    # Closes the gripper
    dafBot.gripper_close()
    # Moves the gantry to set position
    dafBot.move([365,220,0],11000)
    dafBot.move([730,0,0],11000)
    dafBot.move([730,0,-235],11000)
    # Opens the gripper
    dafBot.gripper_open()
    dafBot.gripper_close()
    dafBot.move([730,0,0],11000)