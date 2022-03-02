import os
import shutil
import time
import glob
import torch
from PIL import Image
from imutils import paths


# Initializes the model at the start, run model = load_model
def load_model():
    model = torch.hub.load('./', 'custom', path='yolov5s_best.pt', source='local')
    return model


# Takes in the image from the 'test' folder, and outputs the predicted label - sample at the end
# Images with predicted bounding boxes are saved in the runs folder
def predict_image(image, model):
    img = Image.open(os.path.join('uploads', image))
    results = model(img)
    results.save('runs')
    df_results = results.pandas().xyxy[0]
    df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
    df_results = df_results.sort_values('bboxHt', ascending=True)  # Label with largest bbox height will be last
    pred_list = df_results['name'].to_numpy()
    pred = 'NA'
    # This if statement will ignore Bullseye unless they are the only image detected and select the last label in
    # the list (the last label will be the one with the largest bbox height)
    if pred_list.size != 0:
        for i in pred_list:
            if i != 'Bullseye':
                pred = i
    name_to_id = {
        "NA": 'NA',
        "Bullseye": 10,
        "One": 11,
        "Two": 12,
        "Three": 13,
        "Four": 14,
        "Five": 15,
        "Six": 16,
        "Seven": 17,
        "Eight": 18,
        "Nine": 19,
        "A": 20,
        "B": 21,
        "C": 22,
        "D": 23,
        "E": 24,
        "F": 25,
        "G": 26,
        "H": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35,
        "Up": 36,
        "Down": 37,
        "Right": 38,
        "Left": 39,
        "Up Arrow": 36,
        "Down Arrow": 37,
        "Right Arrow": 38,
        "Left Arrow": 39,
        "Stop": 40
    }
    image_id = str(name_to_id[pred])
    return image_id


# Stitches the previously predicted images in the folder together and saves it into runs/stitched folder
# This function can be called by itself
def stitch_image():
    imgFolder = 'runs'
    stitchedPath = os.path.join(imgFolder, f'stitched-{int(time.time())}.jpeg')

    # find all files that ends with ".jpg" (this won't match the stitched images as we name them ".jpeg")
    imgPaths = glob.glob(os.path.join(imgFolder, "*.jpg"))
    print(imgPaths)
    images = [Image.open(x) for x in imgPaths]
    width, height = zip(*(i.size for i in images))
    total_width = sum(width)
    max_height = max(height)
    stitchedImg = Image.new('RGB', (total_width, max_height))
    x_offset = 0

    # stitch
    for im in images:
        stitchedImg.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    stitchedImg.save(stitchedPath)

    # move original images to "originals" subdirectory
    for img in imgPaths:
        shutil.move(img, os.path.join("runs", "originals", os.path.basename(img)))

    return stitchedImg
