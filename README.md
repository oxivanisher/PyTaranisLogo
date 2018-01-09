This tool lets you create custom taranis boot/start images. The dimensions for the base images are as follows:
* Taranis X7: 128x64px 4bit PNG greyscaled bitmap
* Taranis X9: 212X64px 4bit PNG greyscaled bitmap

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
