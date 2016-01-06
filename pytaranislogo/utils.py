#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://effbot.org/imagingbook/introduction.htm

import Image
import ImageFont
import ImageDraw

import os
import sys
import hashlib
import logging
import yaml

# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S', level=logging.DEBUG)

class PyTanarisLogo(object):

    def __init__(self):
        logging.debug("[Render] Instance created")
        self.cfg = None
        self.title = None
        self.surname = None
        self.prename = None
        self.sourcefile = None
        self.loadConfig()

    def loadConfig(self):
        with open('config/settings.yml', 'r') as f:
            self.cfg = yaml.load(f)
            logging.debug("[Render] Configuration loaded")

    def loadDefaults(self):
        self.title = self.cfg['defaults']['title']['text']
        self.surname = self.cfg['defaults']['surname']['text']
        self.prename = self.cfg['defaults']['prename']['text']
        self.sourcefile = self.cfg['image']['source']

    def renderImage(self):
        image = Image.open(self.sourcefile)
        draw = ImageDraw.Draw(image)
        fontTitle = ImageFont.truetype(self.cfg['fonts']['title']['font'], self.cfg['fonts']['title']['size'])
        fontName = ImageFont.truetype(self.cfg['fonts']['text']['font'], self.cfg['fonts']['text']['size'])

        draw.text((self.cfg['defaults']['title']['width'], self.cfg['defaults']['title']['height']),self.title,(16),font=fontTitle)
        draw.text((self.cfg['defaults']['surname']['width'], self.cfg['defaults']['surname']['height']),self.surname,(16),font=fontName)
        draw.text((self.cfg['defaults']['prename']['width'], self.cfg['defaults']['prename']['height']),self.prename,(16),font=fontName)
        logging.debug("[Render] Rendered image")

        return image

    def run(self):
        myHash = hashlib.md5("%s%s%s%s" % (self.sourcefile.encode('utf-8'), self.title.encode('utf-8'), self.surname.encode('utf-8'), self.prename.encode('utf-8'))).hexdigest()
        outfile = os.path.join(self.cfg['image']['destination'], "%s.%s" % (myHash, self.cfg['image']['extension']))

        logging.debug("[Render] Surname:      %s" % (self.surname))
        logging.debug("[Render] Prename:      %s" % (self.prename))
        logging.debug("[Render] Title:        %s" % (self.title))
        logging.debug("[Render] Hash:         %s" % (myHash))
        logging.debug("[Render] Sourcefile:   %s" % (self.sourcefile))
        logging.debug("[Render] Outfile:      %s" % (outfile))

        # only render if file not already exists
        if os.path.isfile(outfile):
            logging.info("[Render] Already existing file: %s" % (outfile))
        else:
            logging.info("[Render] Rendering not existing file: %s" % (outfile))

            image = self.renderImage()

            try:
                image.save(outfile)
            except IOError:
                logging.error("[Render] Cannot save to: %s" % (outfile))

        return myHash

if __name__ == "__main__":
    plr = PyTanarisLogo()
    plr.loadDefaults()
    plr.run()