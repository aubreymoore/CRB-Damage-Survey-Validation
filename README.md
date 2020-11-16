# CRB-Damage-Survey-Validation
Coconut rhinoceros beetle damage index assessed by object detectors is validated by human experts. 

## Selecting Random Images of Trees Located in Videos

```bash
aubrey@tensorbook2:~/Desktop/CRB-Damage-Survey-Validation$ python3 extract_images.py -h
usage: extract_images.py [-h] [-e] IMAGEDIR [VIDEODIR] [DATABASE] [SAMPLESIZE]

Aubrey Moore 2020-11-17

This script selects tree images at random (without replacement) from the SpatiaLite database specified by the global
variable DATABASE. These images are stored in a folder specified by IMAGEDIR, along with a CSV file, index.csv,
which contains metadata for the images.

If the flag, equal_samples, is used, SAMPLESIZE//5 tree objects are selected for each of the 5 damage classes.
Otherwise, SAMPLESIZE tree objects are randomly selected from the total population of tree objects.

positional arguments:
  IMAGEDIR
  VIDEODIR             [/home/aubrey/Desktop/Guam-CRB-damage-
                       map-2020-10/videos]
  DATABASE             [/home/aubrey/Desktop/Guam-CRB-damage-
                       map-2020-10/Guam01.db]
  SAMPLESIZE           [10]

optional arguments:
  -h, --help           show this help message and exit
  -e, --equal-samples  equal sample size for each damage index
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

## Doin It

https://crbturkle.pythonanywhere.com/admin/turkle/project/add/