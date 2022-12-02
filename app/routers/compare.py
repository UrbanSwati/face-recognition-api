from fastapi import APIRouter, status
from fastapi import FastAPI, status, HTTPException
import cv2
import face_recognition
import boto3

import base64
import numpy as np

from app.util import BUCKET_NAME, Item

client = boto3.client('s3')

router = APIRouter()

@router.post("/compare", status_code=status.HTTP_200_OK)
async def compare_images(item: Item):
    images_to_compare_with = []
    # Gets list of files from S3 Bucket
    response = client.list_objects_v2(Bucket=BUCKET_NAME)
    for image in response['Contents']:
        image_key = image['Key']

        # Get file from bucket
        image_object = client.get_object(Bucket=BUCKET_NAME, Key=image_key)
        contents = image_object.get('Body').read()

        # Loads file in array of images which we will compare with
        img_np = cv2.imdecode(np.asarray(bytearray(contents)), cv2.IMREAD_COLOR)

        img_encoding = face_recognition.face_encodings(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))[0]
        images_to_compare_with.append(img_encoding)

    # Reads sent file and compare with list of files found on S3 using OpenCV AI Model
    compare_img_encoding = face_recognition.face_encodings(cv2.cvtColor(data_uri_to_cv2_img(item.content), cv2.COLOR_BGR2RGB))[0]

    # Returns a list of booleans, where True it means the images match
    result = face_recognition.compare_faces(images_to_compare_with, compare_img_encoding)

    if True in result:
        return {"detail": "User face found successfully"}
    raise HTTPException(status_code=404, detail="User not found")

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img