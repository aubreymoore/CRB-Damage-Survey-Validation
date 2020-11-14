#!/bin/bash

echo "Bash version ${BASH_VERSION}"

# Usage: ./randy.sh /home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/Guam01.db

spatialite -batch $1 <<EOF
DROP TABLE IF EXISTS randy;
CREATE TABLE randy (video, frame_number, tree_id, damage_index, bounding_box);
EOF

# Get 20 random records, without replacement, for each damage group

for i in {0..4}
do
spatialite -batch $1 <<EOF
INSERT INTO randy
SELECT 
    videos.name AS video, 
    frames.frame_number,
    trees.id AS tree_id, 
    trees.damage_index, 
    AsText(trees.geometry) AS bounding_box
FROM trees, frames, videos 
WHERE damage_index = $i 
    AND trees.frame_id=frames.id
    AND frames.video_id=videos.id
ORDER BY RANDOM() 
LIMIT 20;
EOF
done

# Shuffle records in the randy table and write to a CSV file

spatialite -batch $1 <<EOF
.headers on
.mode csv
.separator '|'
.output random-trees.csv
SELECT * FROM randy ORDER BY RANDOM();
.output stdout
EOF

echo 'Data written to random-trees.csv'





