from gantry import Gantry

dafBot = Gantry('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303931351A071E2-if00')
dafBot.send_command('$HZ', 1)
# dafBot.move_new([10,10,10], 8000)

# dafBot.send_command('G28 X', 1)
# dafBot.send_command('$HX', 1)

# dafBot.homex()
# dafBot.move_new([10,10,0],11000)
# while True:
#     dafBot.move_new([10,10,10],11000)
    # dafBot.move_new([0,0,0],11000)
    