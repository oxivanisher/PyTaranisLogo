import os
import sys

os.environ['TARANISLOGO_CFG'] = "USERHOME/www_data/wsgi/pytaranislogo.cfg"

sys.path.insert(0, 'USERHOME/git_checkouts/PyTaranisLogo/')

from pytaranislogo import app as application
