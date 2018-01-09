This tool lets you create custom taranis boot/start images. The dimensions for the base images are as follows:
* Taranis X7: 128x64px 4bit PNG greyscaled bitmap
* Taranis X9: 212X64px 4bit PNG greyscaled bitmap

## How to install
* Setup things dist/pytaranislogo.cfg (copy from pytaranislogo.cfg.example)
* Setup things config/settings.yml (copy from settings.yml.example)
* Download FREESCPT.TFF from http://fontzone.net/download/freestyle-script to resources/
* For each instance:
** Generate your base image from dist/x9-empty.xcf and copy it to `resources/logoImage` (from `settings.yml`)
** Generate (download) the example image and copy/convert it to `static/img/exampleImage` (from `settings.yml`)
** Copy a background image to `static/img/backgroundImage` (from `settings.yml`)
* Setup logrotate to rotate `log/*.log`


### Python Requirements
* Flask
* Imaging Library


### To fix Pillow problems > Pillow is a PIL replacement because PIL is EOL:
  apt-get install libfreetype6-dev
  apt-get purge python-imaging
  pip uninstall pillow
  pip install --no-cache-dir pillow
  /etc/init.d/apache2 restart
