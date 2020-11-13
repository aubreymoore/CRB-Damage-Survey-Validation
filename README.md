# CRB-Damage-Survey-Validation
Coconut rhinoceros beetle damage index assessed by object detectors is validated by human experts. 

## Deploying Turkle on PythonAnywhere

Turkle, a FOSS clone of Amazon Mechanical Turk implemented using Django, was hosted in a free PythonAnywhere account following directions in [Deploying an existing Django project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/).

```bash
git clone https://github.com/hltcoe/turkle.git
```
    
**/var/www/crbturkle_pythonanywhere_com_wsgi.py**
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

**Modifications to /home/crbturkle/turkle/turkle_site/settings.py**
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

    
    
