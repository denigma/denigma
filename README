===============
Denigma Project
===============

Denigma is the digital Engima destined to decipher life. This repository is planting its seed.


Setting up Denigma
==================
In order to set up Denigma locally just do the following 
(Ubuntu or at least a UNIX environment is recommanded):

1. Git in:
Go to the GIT bootcamp: https://github.com/
In brief on UNIX:

sudo apt-get git # install git

Configure git with your name and e-mail:
git config --global user.name "FULL NAME"
git config --global user.email email@address.com

2. Fork Denigma:
git clone https://github.com/hevok/denigma

3. Start Denigma:
cd denigma
virtualenv env
. env/bin/activate
pip install -r denigma/requirements/project.txt
denigma/manage.py syncdb --all
denigma/manage.py migrate --fake
denigma/manage.py runserver

4. Change Denigma:
git commit -am "Brief description of the change."
git push origin master

5. Keep Denigma Updated:
git checkout master # Update to the latest version.
git pull # Pull it from master.
