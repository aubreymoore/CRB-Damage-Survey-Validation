"""

extract_images.py

Aubrey Moore 2020-11-17

This script selects tree images at random (without replacement) from the SpatiaLite database specified by the global
variable DATABASE. These images are stored in a folder specified by IMAGEDIR, along with a CSV file, index.csv,
which contains metadata for the images.

If the flag, equal_samples, is used, SAMPLESIZE//5 tree objects are selected for each of the 5 damage classes.
Otherwise, SAMPLESIZE tree objects are randomly selected from the total population of tree objects.

Example:

python3 extract_images.py \\
batch1 \\
/home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/videos \\
/home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/Guam01.db \\
https://github.com/aubreymoore/CRB-Damage-Survey-Validation \\
100

Usage:
  extract_images.py IMAGEDIR VIDEODIR DATABASE GITHUBURL SAMPLESIZE [--equal_samples]
  extract_images.py -h | --help

Options:
  -h, --help           Show this screen.
"""

from docopt import docopt
import pandas as pd
import cv2
import re
import os
import subprocess
import spatialite


def run_randy(equal_samples):
    """
    This function creates a new table called 'randy' within the SpatiaLite database DATABASE.
    Randy is populated with data for tree objects selected at random (without replacement).
    If equal_samples is True, equal numbers of tree objects are selected for each of the 5 damage classes.
    Otherwise, the random sample is drawn from the total population of tree objects.
    """

    def dbdo(sql, options=''):
        subprocess.run(f'spatialite {options} {DATABASE} "{sql}"', shell=True)

    dbdo('DROP TABLE IF EXISTS randy;')
    dbdo('CREATE TABLE randy (video, frame_number, tree_id, damage_index, bounding_box);')

    if equal_samples:
        limit = SAMPLESIZE//5
        for damage_index in range(5):
            dbdo(f"""
                INSERT INTO randy
                SELECT
                    videos.name AS video,
                    frames.frame_number,
                    trees.id AS tree_id,
                    trees.damage_index,
                    AsText(trees.geometry) AS bounding_box
                FROM trees, frames, videos
                WHERE damage_index = {damage_index}
                    AND trees.frame_id=frames.id
                    AND frames.video_id=videos.id
                ORDER BY RANDOM()
                LIMIT {limit};
                """)
    else:
        dbdo(f"""
            INSERT INTO randy
            SELECT
                videos.name AS video,
                frames.frame_number,
                trees.id AS tree_id,
                trees.damage_index,
                AsText(trees.geometry) AS bounding_box
            FROM trees, frames, videos
            WHERE trees.frame_id=frames.id
                AND frames.video_id=videos.id
            ORDER BY RANDOM()
            LIMIT {SAMPLESIZE};
            """)


def extract_image(image_dir, image_file_name, video, frame_number, tree_id, xtl, ytl, xbr, ybr):
    cap = cv2.VideoCapture(video)
    cap.set(1, frame_number)
    _, frame = cap.read()
    img = frame[ytl:ybr, xtl:xbr]
    output_path = f'{image_dir}/{image_file_name}'
    cv2.imwrite(output_path, img)
    if not os.path.exists(output_path):
        print(f'ERROR: {output_path} does not exit.')

# Helper functions for wrangling data within a pandas data frame

def parse_bounding_box_column(r):
    r['xtl'], r['ytl'], r['xbr'], r['ybr'] = [int(i) for i in re.findall('\d+', r.bounding_box)]
    return r

def format_image_file_name(r):
    return f'{r.name:03}.jpg'

def format_image_url(r):
    # Example: https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/batch1/000.jpg
    return f'{GITHUBURL}/raw/main/{IMAGEDIR}/{r.image_file_name}'


# MAIN

# Get command line parameters

args = docopt(__doc__)
IMAGEDIR = args['IMAGEDIR']
VIDEODIR = args['VIDEODIR']
DATABASE = args['DATABASE']
GITHUBURL = args['GITHUBURL']
SAMPLESIZE = args['SAMPLESIZE']
equal_samples = args['--equal_samples']

# Pre-run checklist

if equal_samples:
    assert SAMPLESIZE%5==0, 'SAMPLESIZE must be a multiple of 5 when the equal_samples flag is set'

assert os.path.exists(VIDEODIR), f'VIDEODIR does not exist at {VIDEODIR}'

assert not os.path.exists(IMAGEDIR), \
    f'IMAGEDIR already exists at {IMAGEDIR}. Either delete IMAGEDIR or specify a new one.'

assert os.path.exists(DATABASE), f'DATABASE does not exist at {DATABASE}'

run_randy(equal_samples)
os.mkdir(IMAGEDIR)
conn = spatialite.connect(DATABASE)
df = pd.read_sql('SELECT * FROM randy ORDER BY RANDOM();', conn)
df = df.apply(parse_bounding_box_column, axis=1)
df.drop('bounding_box', axis=1, inplace=True)
df['image_file_name'] = df.apply(format_image_file_name, axis=1)
df['image_url'] = df.apply(format_image_url, axis=1)
df.to_csv(f'{IMAGEDIR}/index.csv', index=False)
for i, r in df.iterrows():
    video = f'{VIDEODIR}/{r.video}'
    try:
        extract_image(IMAGEDIR, r.image_file_name, video, r.frame_number, r.tree_id, r.xtl, r.ytl, r.xbr, r.ybr)
    except:
        print(f'ERROR: Could not extract {video} frame {frame_number} tree image{tree_id}')
print('FINISHED')
