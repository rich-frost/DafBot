from gantry import Gantry
from gantry import FindCOMPort as FCOM
import time
import sys

dafBot = Gantry(FCOM())
# Sets home position for all Vectors, assigns 0,0,0
dafBot.home_all()

# Main Loop
while True:
    # Moves the gantry to set position
    dafBot.move([365,220,0],11000)
    dafBot.move([365,220,-235],11000)
    # Closes the gripper
    dafBot.gripper_close()
    # Moves the gantry to set position
    dafBot.move([365,220,0],11000)
    dafBot.move([0,0,0],11000)
    # Opens the gripper
    dafBot.gripper_open()
