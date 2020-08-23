import requests
from PIL import Image
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
    image = png.from_array(np, 'L')
    print(image)
    print(image_data)
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    faces = response.json()
    print(faces)