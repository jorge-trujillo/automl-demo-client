#!/bin/env python3

import sys
import cv2
import pyshine as ps
import base64
import requests
import json

from google.auth.transport import requests as googleauth
from google.oauth2 import service_account

LABEL = "label"
CONFIDENCE = "confidence"
API_URL = "https://automl.googleapis.com/v1beta1/projects/208465506633/locations/us-central1/models/ICN1844858465617444864:predict"
CREDENTIAL_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

def getToken(sa_file):
    credentials = service_account.Credentials.from_service_account_file(sa_file, scopes=CREDENTIAL_SCOPES)
    credentials.refresh(googleauth.Request())
    return credentials.token

# Add text lines to an image
def writeTextToImage(text, image):
    top_margin = 30
    line_height = 70
    row = 0

    text_lines = text.split('\n')    
    for line in text_lines:
        image = ps.putBText(
            image, 
            line, 
            text_offset_x=20, 
            text_offset_y=(top_margin + line_height*row),
            vspace=15, 
            hspace=10, 
            font_scale=1.3,
            background_RGB=(0,0,0),
            text_RGB=(255,255,255),
            thickness = 2,
            alpha = 0.5
        )
        row += 1
    return image

# Hit Google vision API with a REST request
def getLabel(token, image):
    print(f"Calling API with data of size: {len(image)} bytes")

    headers = {
        "Authorization": "Bearer " + token
        }
    data = {
        "payload": {
            "image": {
                "imageBytes": image
            }
        }
    }
    
    response = requests.post(API_URL, headers = headers, json = data)
    print(f"API responded with code: {response.status_code}")

    if response.status_code == 200:
        response_json = response.json()

        return {
            LABEL: response_json["payload"][0]["displayName"],
            CONFIDENCE: response_json["payload"][0]["classification"]["score"]
        }
    else:
        print(f"Error ocurred reading from API!\n\n{response.text}")
        sys.exit(1)

# ------------------------------

if len(sys.argv) < 3:
    print("Arguments are: ")
    print("run_eval.py <service_account> <image_path>")
    sys.exit(1)

sa_path = sys.argv[1]
image_path = sys.argv[2]

print (f'Evaluating image {image_path}')

# Get token
token_string = getToken(sa_path)

# Get API response
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

evaluation = getLabel(token_string, encoded_string)

# Image
confidence = ""
if evaluation[CONFIDENCE] > 0.9:
    confidence = "HIGH"
else:
    confidence = "LOW"
confidence += f" ({str(round(evaluation[CONFIDENCE], 2))})"

img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
img = writeTextToImage(f"Animal is a: {evaluation[LABEL]}\nConfidence is: {confidence}", img)

cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.destroyAllWindows() # destroy all windows
#sys.exit() # to exit from all the processes
