import requests
import base64
from PIL import Image
from io import BytesIO
import os
import FaceAPIConfig as cnfg
import png

image_path = os.path.join('/Users/roy/hackthe6ix/CLAAS/CLAAS/RH_Louise_Lillian_Gish.PNG')
image_data = open(image_path, 'rb')

sub_key, face_api_url = cnfg.config()

headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': sub_key}

params = {
    'returnFaceId': True,
    'returnFaceLandmarks': True,
    'returnFaceAttributions': 'headPose, smile, emotion'
}

def getData(np):
    #print(np)
    try:
        Image.fromarray(np).save('me.PNG')
        imagePath = os.path.join('/Users/roy/hackthe6ix/CLAAS/CLAAS/me.PNG')
        imageData = open(imagePath, 'rb')
    except IOError:
        print("don't worry")

    response = requests.post(face_api_url, params=params, headers=headers, data=imageData)
    response.raise_for_status()
    faces = response.json()
    return(faces)