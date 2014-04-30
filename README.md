# Status.ctrl

## Easy-to-use open-source status web app'

*Inspired by status.io & statuspage.io*

![Preview](https://bytebucket.org/Dsensei/status.ctrl/raw/3ed59e942347116c1d2251d02ad5c118617ab734/static/img/preview.png)

## Features

### V0.1

+ Multiple websites monitoring on the same page
+ Highcharts integration
+ Average values
+ Tools:
	+ Website tools:
		+ Availability
		+ Ping (Website response time)

## Install instructions

### Virtualenv way

*Why virtualenv ? Checkout out the introduction : [link](http://www.virtualenv.org/en/latest/virtualenv.html)*

+ First you'll need python >= 3.0 (3.4 is available so go for it!), type the following commands:
	+ Debian `apt-get install python3 python3-pip`
	+ Archlinux `pacman -S python python-pip; pip install virtualenv setuptools`

+ Move in the folder you want it to be installed
+ Use `virtualenv Status.ctrl` to create a virtual environment for the project.
+ `cd Status.ctrl`
+ Enter the virtual environment using `source bin/activate`
+ Clone this repository: `git clone https://Dsensei@bitbucket.org/Dsensei/status.ctrl.git`

Your directory structure should now look like this:

```
path/Status.ctrl/ (virtualenv root)
    bin/
    include/
    lib/
    status.ctrl/
        README.md
        requirements.txt
        static/
        ...
```

+ cd in the freshly created status.ctrl folder
+ You will also need some python packages, you must install them if you want Status.ctrl to work smoothly :
+ type `pip install -r requirements.txt`
+ make sure that you installed all of them with `pip freeze`

To install statics (templates/css/js/img/...)

+ Use the following command `python manage.py collectstatic` being in epiportal/web/ folder.

To create your database:

+ You will have to synchronize the database with `python manage.py syncdb`.

+ Finally launch default fixtures using following commands :
    + `python manage.py shell`
    + `from monitor import fixtures`
+ If everything worked well you are now able to run you server... 

## Running your server

TODO