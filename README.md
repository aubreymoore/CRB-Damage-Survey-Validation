# CRB-Damage-Survey-Validation
Coconut rhinoceros beetle damage index assessed by object detectors is validated by human experts. 

## Selecting Random Images of Trees Located in Videos

**randy.sh** (in this repo)
```bash
#!/bin/bash

echo "Bash version ${BASH_VERSION}"

spatialite -batch $1 <<EOF
DROP TABLE IF EXISTS randy;
CREATE TABLE randy (video, frame_number, damage_index, bounding_box);
EOF

# Get 20 random records, without replacement, for each damage group

for i in {0..4}
do
spatialite -batch $1 <<EOF
INSERT INTO randy
SELECT 
    videos.name AS video, 
    frames.frame_number, 
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
```

## Deploying Turkle on PythonAnywhere

Turkle, a FOSS clone of Amazon Mechanical Turk implemented using Django, was hosted in a free PythonAnywhere account following directions in [Deploying an existing Django project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/).

```bash
git clone https://github.com/hltcoe/turkle.git
```
    
**/var/www/crbturkle_pythonanywhere_com_wsgi.py** (in PythonAnywhere free account)
```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

path = '/home/crbturkle/turkle'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'turkle_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Modifications to /home/crbturkle/turkle/turkle_site/settings.py** (in PythonAnywhere free account)
```python
...
STATIC_ROOT = '/home/crbturkle/turkle/turkle/static'
STATIC_URL = '/static/'
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/crbturkle/turkle/db.sqlite3',
    }
}
...
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Pacific/Guam'
```

## Extracting Images from Videos

 ## Creating a Turkle Job
 
    
    
