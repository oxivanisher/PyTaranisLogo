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

# logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S', level=self.log.DEBUG)

class PyTanarisLogo(object):

    def __init__(self, cfg = None):
        self.log = self.log.getLogger(__name__)
        self.log.debug("[Render] Instance created")
        self.cfg = None
        self.title = None
        self.surname = None
        self.prename = None
        self.extension = None
        self.sourcefile = None
        self.resourcePath = None
        self.destinationPath = None
        if cfg:
            self.cfg = cfg
            self.parseConfig()
        else:
            self.loadConfig()

    def loadConfig(self):
        with open('config/settings.yml', 'r') as f:
            self.parseConfig(yaml.load(f))
            self.log.debug("[Render] Configuration loaded")

    def parseConfig(self):
        self.title = self.cfg['texts']['title']['text']
        self.surname = self.cfg['texts']['surname']['text']
        self.prename = self.cfg['texts']['prename']['text']
        self.extension = self.cfg['defaults']['extension']
        self.sourcefile = self.cfg['defaults']['defaultImage']
        self.resourcePath = self.cfg['defaults']['resourcesPath']
        self.destinationPath = self.cfg['defaults']['destinationPath']

    def renderImage(self):
        image = Image.open(os.path.join(self.resourcePath, self.sourcefile))
        draw = ImageDraw.Draw(image)

        titleFontPath = os.path.join(self.resourcePath, self.cfg['fonts']['title']['font'])
        self.log.debug("[Render] Loading title font: %s" % (titleFontPath))
        titleFont = ImageFont.truetype(titleFontPath, self.cfg['fonts']['title']['size'])

        textFontPath = os.path.join(self.resourcePath, self.cfg['fonts']['text']['font'])
        self.log.debug("[Render] Loading text font: %s" % (textFontPath))
        textFont = ImageFont.truetype(textFontPath, self.cfg['fonts']['text']['size'])

        draw.text((self.cfg['texts']['title']['width'], self.cfg['texts']['title']['height']),self.title,(16),font=titleFont)
        draw.text((self.cfg['texts']['surname']['width'], self.cfg['texts']['surname']['height']),self.surname,(16),font=textFont)
        draw.text((self.cfg['texts']['prename']['width'], self.cfg['texts']['prename']['height']),self.prename,(16),font=textFont)

        self.log.debug("[Render] Rendered image")

        return image

    def run(self):
        myHash = hashlib.md5("%s%s%s%s" % (self.sourcefile.encode('utf-8'), self.title.encode('utf-8'), self.surname.encode('utf-8'), self.prename.encode('utf-8'))).hexdigest()
        outfile = os.path.join(self.destinationPath, "%s.%s" % (myHash, self.extension))

        self.log.debug("[Render] Surname:      %s" % (self.surname))
        self.log.debug("[Render] Prename:      %s" % (self.prename))
        self.log.debug("[Render] Title:        %s" % (self.title))
        self.log.debug("[Render] Hash:         %s" % (myHash))
        self.log.debug("[Render] Sourcefile:   %s" % (self.sourcefile))
        self.log.debug("[Render] Outfile:      %s" % (outfile))

        # only render if file not already exists
        if os.path.isfile(outfile):
            self.log.info("[Render] Already existing file: %s" % (outfile))
        else:
            self.log.info("[Render] Rendering not existing file: %s" % (outfile))

            image = self.renderImage()

            try:
                image.save(outfile)
            except IOError:
                self.log.error("[Render] Cannot save to: %s" % (outfile))

        return myHash

if __name__ == "__main__":
    plr = PyTanarisLogo()
    plr.loadDefaults()
    plr.run()