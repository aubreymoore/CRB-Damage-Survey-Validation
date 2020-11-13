# CRB-Damage-Survey-Validation
Coconut rhinoceros beetle damage index assessed by object detectors is validated by human experts. 

## Deploying Turkle on PythonAnywhere

Turkle, a FOSS clone of Amazon Mechanical Turk implemented using Django, was hosted in a free PythonAnywhere account following directions in [Deploying an existing Django project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/).

    git clone https://github.com/hltcoe/turkle.git
    
**/var/www/crbturkle_pythonanywhere_com_wsgi.py**
```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/crbturkle/mysite/mysite/settings.py'
# and your manage.py is is at '/home/crbturkle/mysite/manage.py'
path = '/home/crbturkle/turkle'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'turkle_site.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

    
    
