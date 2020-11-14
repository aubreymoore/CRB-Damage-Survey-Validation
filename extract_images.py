import pandas as pd
import cv2
import re
import os

CSVFILE='/home/aubrey/Desktop/CRB-Damage-Survey-Validation/random-trees.csv'
VIDEODIR='/home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/videos'
IMAGEDIR='/home/aubrey/Desktop/CRB-Damage-Survey-Validation/random_trees'

def extract_image(video, frame_number, tree_id, xtl, ytl, xbr, ybr):
    cap = cv2.VideoCapture(video)
    cap.set(1, frame_number)
    _, frame = cap.read()
    img = frame[ytl:ybr, xtl:xbr]
    output_path = f'{IMAGEDIR}/t{tree_id}.jpg'
    cv2.imwrite(output_path, img)
    if not os.path.exists(output_path):
        print(f'ERROR: {output_path} does not exit.')

# MAIN

os.makedirs(IMAGEDIR, exist_ok=True)
df = pd.read_csv(CSVFILE, sep='|')
for _, r in df.iterrows():
    video = f'{VIDEODIR}/{r.video}'
    frame_number = r.frame_number
    tree_id = r.tree_id
    xtl, ytl, xbr, ybr = [int(i) for i in re.findall('\d+', r.bounding_box)]
    try:
        extract_image(video, frame_number, tree_id, xtl, ytl, xbr, ybr)
    except:
        print(f'ERROR: Could not extract {video} frame {frame_number} tree image{tree_id}')


