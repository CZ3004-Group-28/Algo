import cv2
import torch
import os
from PIL import Image
import time
import pandas


def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_best.pt')
    return model


def predict_image(image, model):
    img = Image.open(os.path.join('uploads', image))
    results = model(img)
    pred_list = results.pandas().xyxy[0]['name'].to_numpy()
    pred = 'NA'
    for i in pred_list:
        if i != 'Bullseye':
            pred = i
    return pred

# model = load_model()
# image = '2_1.jpg'
# print(predict_image(image,model))
