from gantry import Gantry

dafBot = Gantry('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_75735303931351A071E2-if00')
dafBot.homex()
# while True:
#     dafBot.move([100,100,100,8000])
#     dafBot.move([0,0,0,8000])
    