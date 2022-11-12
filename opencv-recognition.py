import numpy as np
import cv2
import time
import math
foundcam = False
camcheck = 0


#while foundcam != True:
#    print(camcheck)
#    if camcheck > 10:
#        camcheck = 0
#    try:
#        camfeed = cv2.VideoCapture(camcheck)
#        et, initialimg = camfeed.read()
#        #print(initialimg)
#        time.sleep(1)
#        cv2.imshow('ahhh', initialimg)
#        cv2.waitKey(2)
#    except Exception as e:
#        print(e)
#        camcheck = camcheck + 1
#        continue
#    print("Is this the correct video feed? Y/N")
#    yesno = input("")
#    if yesno == "Y":
#        foundcam = True
#        cv2.destroyAllWindows()
#    elif yesno == "N":
#        camcheck = camcheck +1
#        cv2.destroyAllWindows()

camfeed = cv2.VideoCapture('/dev/v4l/by-id/usb-OmniVision_Technologies__Inc._USB_Camera-B4.09.24.1-video-index0')
time.sleep(2)
ret, img = camfeed.read()
ret, img = camfeed.read()
ret, img = camfeed.read()

while True:
    ret, img = camfeed.read()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imggray,127,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)
        if (area < 2000) & (area > 400):
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.drawContours(img, cnt, -1, (0, 255, 0), 2)
                cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(img, "daffodil", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    #inrng = cv2.inRange(img, (22,0,0), (163,49,123))
    cv2.circle(img, (int(math.floor(img.shape[1]/2)), int(math.floor(img.shape[0]/2))), 7, (0, 0, 255), -1)
    cv2.putText(img, "center", (int(math.floor(img.shape[1]/2)), int(math.floor(img.shape[0]/2))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.imshow('ahhh', img)
    break
    
cv2.waitKey(100000)
cv2.destroyAllWindows()
