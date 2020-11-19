# CRB-Damage-Survey-Validation

In this project I evaluate results of the first automated roadside videosurvey to measure coconut rhinoceros beetle (CRB) damage on Guam. Survey results are available in a another GitHub repo, https://github.com/aubreymoore/Guam-CRB-damage-map-2020-10, which stores videos using [LFS](https://git-lfs.github.com/)  and a SpatiaLite survey database.  The repo also hosts an [online interactive map](https://aubreymoore.github.io/Guam-CRB-damage-map-2020-10/).

## METHODS

I evaluated survey results using the following steps:

* Step 1: Random tree images were extracted at random from the survey videos.
* Step 2:  I installed Turkle, a FOSS clone of Amazon's Mechanical Turk.on a free PythonAnywhere account to facilitate assigning a CRB damage level index to tree images.
* Step 3: Analysis was performed using a Jupyter Notebook which generated a confusion matrix.

### Step 1: Selecting Random Images of Trees Located in Videos

I used a Python script to generate a random selection of images extracted from survey videos:

```
python3 extract_images.py batch1 \
/home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/videos \
/home/aubrey/Desktop/Guam-CRB-damage-map-2020-10/Guam01.db \
https://github.com/aubreymoore/CRB-Damage-Survey-Validation 100
```
```
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


### Step 2: Deploying Turkle on PythonAnywhere

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

#### Turkle Screen Shot

This Turkle site uses an HTML template and CSV data file listed below.

![](https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/turkle-screenshot.png)

#### HTML Template (roadside.html)

```html
<!--
    HTML template that uses images and variable in instructions.

    This template uses Bootstrap and jQuery.
    The JavaScript and CSS are loaded from public CDNs.

    The CSV input file should have column named "image_url".
    The template then uses ${image_url} in an img tag.

    The CSV output file will have columns for Input.object, Input.image and Answer.answer
    in addition to metadata columns.
-->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script>
$(document).ready(function() {
  // process a click on an option button
  $('.option').on('click', function(event) {
    // copy answer to hidden input
    $('input[name="answer"]').val($(this).html());
    // erase any selected button
    $('.option').removeClass('btn-info');
    // highlight the current button
    $(this).addClass('btn-info');
    // don't submit the form
    event.preventDefault();
  });
});
</script>

<div class="container mt-2">
  <h4>Please rate damage to coconut tree(s) in the image using 
    <a href="https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/jackson-crb-damage-index-5.pdf">
    Jackson's CRB Damage Index</a>.<br/>You can add
    an optional note for any image, but please ensure that you do so if you select 
    <b>cannot determine</b>.</h4>
  <div class="row">
    <div class="col-8">
<!--
      <img src="${image_url}" class="img-fluid" alt="Responsive image" border="1" height="600">
-->
      <img src="${image_url}" border="1" height="500">
    </div>
    <div class="col-4">
      <h5>CRB damage rating</h5>
      <div class="form-group">
        <div class="btn-group-vertical">
          <button class="btn btn-secondary option">zero</button>
          <button class="btn btn-secondary option">light</button>
          <button class="btn btn-secondary option">medium</button>
          <button class="btn btn-secondary option">high</button>
          <button class="btn btn-secondary option">non_recoverable</button>
          <button class="btn btn-secondary option">cannot determine</button>
        </div>
      </div>
      <h5>Note (optional)</h5>
      <div class="form-group">
          <input type="text" name="note" class="form-control"/>
      </div>
      <input type="hidden" name="answer">
      <div class="form-group">
        <input type="submit" class="btn btn-primary" value="Submit">
      </div>
    </div>
  </div>
</div>
```

#### CSV file (batch1/index.csv)

Note that tree images are served from this repo.

```csv
video,frame_number,tree_id,damage_index,xtl,ytl,xbr,ybr,image_file_name,image_url
20201001_095445.mp4,1292,4717,1,563,379,937,696,000.jpg,https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/batch1/000.jpg
20201005_130825.mp4,3876,19346,0,484,353,928,962,001.jpg,https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/batch1/001.jpg
...
```

### Step 3: Generating a Confusion Matrix

The confusion matrix is generated by [this Jupyter notebook](https://github.com/aubreymoore/CRB-Damage-Survey-Validation/blob/main/confusion_matrix.ipynb).

## RESULTS AND DISCUSSION

![](https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/cm_before.png) 

With an overall accuracy of 51%, results from automated assignment of the CRB damage index to tree images are disappointing.  The biggest problem is an extremely high false positive rate for CRB damage detection. The human labeled 34 trees with **zero damage**. However, the machine labeled 25 of these same trees as **light** and 2 of them as **medium**.

Automated assignment of CRB damage index is performed by an object detector which locates images of coconut palms in videos and assigns a damage rating to each palm detected. A second object detector finds v-shaped cuts within the detect tree images. Initially, presence of v-shaped cuts in a tree imags was not used in rating damage. 

It may be possible to improve accuracy by counting v-shaped cuts to each tree object. The essential idea here is that tree images classified as having **zero** damage must have have zero v-shaped cuts and trees classified as **light** or **medium** damage must have at least one v-shaped cut. Application of the following rules in post-processing may improve accuracy:
        
 **Rule 1.** Trees with **zero damage (0)** must have no v-shaped cuts. Trees breaking this rule will be promoted to **light damage (1)**. 
 
     SET damage_index=1 WHERE (damage_index=0 AND vcut_count>0)
 
 **Rule 2.** Trees with **light damage (1)** must have one or more v-shaped cuts. Trees breaking this rule will be demoted to **zero damage (0)**. 
 
    SET damage_index=0 WHERE damage_index=1 and vcut_count=0
 
 **Rule 3.** Trees with **medium damage (2)** must have one or more v-shaped cuts. Trees breaking this rule will be demoted to **zero damage (0)**. 
 
     SET damage_index=0 WHERE damage_index=2 and vcut_count=0

### Improvement After Including Info from the V-shaped Object Detector Before Assigning Damage Levels

See  the [Jupyter notebook](https://github.com/aubreymoore/CRB-Damage-Survey-Validation/blob/main/confusion_matrix.ipynb) which I evaluated results after applying the above rules. A marked improvement was achieved. After applying the 3 rules, accuracy was increased from 51% to 68% and the false positive rate decreased from 39% to 1%.

![](https://github.com/aubreymoore/CRB-Damage-Survey-Validation/raw/main/cm_after.png) 

