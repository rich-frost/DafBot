from gantry import Gantry
from gantry import FindCOMPort as FCOM
import time
import sys

import json
import os
import io
#getting modules needed to access api
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import requests # pip install requests
from PIL import Image, ImageDraw, ImageFont

#getting authorisation and confirming credentials from the azure website
credential = json.load(open('credential.json'))
API_KEY = credential['API_KEY']
ENDPOINT = credential['ENDPOINT']# need to be altered for the correct api
#accessing cv client
cv_client = ComputerVisionClient(ENDPOINT,CognitiveServicesCredentials(API_KEY))
#url image
#list1 = ['yellow']
image_url ='https://cdn.discordapp.com/attachments/1041016713392693400/1041016904241918063/thumbnail_IMG_5958.jpg' 

#using analyse image function
response = cv_client.analyze_image(
    url = image_url,
    visual_features=[VisualFeatureTypes (objects: object =daffodil)],
    raw = True
)
operationLocation = response.headers['Operation-location']
operation_id = operationLocation.split('/')[-1]
result = cv_client.get_read_result(operation_id)

print(result)














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
