### Font from:
http://fontzone.net/download/freestyle-script

### Original Image by:
Mitch Rabada

### Python Requirements:
*Flask
*Imaging Library

### To fix Pillow problems > Pillow is a PIL replacement because PIL is EOL:
  apt-get install libfreetype6-dev
  apt-get purge python-imaging
  pip uninstall pillow
  pip install --no-cache-dir pillow
  /etc/init.d/apache2 restart
