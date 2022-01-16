import json 
import os
from PIL import Image

with open('../images/annotations.json', 'r') as fp:
    data = json.load(fp)
    fp.flush()
    fp.close()

for item in data:
    image_path = item['filepath']
    imageName = os.path.basename(item['filepath'])
    
    im = Image.open(image_path)
    for box in item['boxList']:
        x = box['x']
        y = box['y']
        width = box['width']
        height = box['height']
        
        if box['label'] is not None:

            label = box['label']['name']
            path_bb = f'../images/box_images/{imageName}-bb-{x}x{y}-{x+width}-{y+height}-{label}.jpg'   
            im_crop = im.crop((x, y, x+width, y+height))
            im_crop.save(path_bb, "JPEG")

