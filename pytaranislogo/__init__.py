#!/usr/bin/env python
# -*- coding: utf-8 -*-

# imports
import sys
import os
import logging
import time

from utils import *

# logging to file
myPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
logPath = os.path.join(myPath, 'log/pytaranislogo.log')
logging.basicConfig(filename=logPath, format='%(asctime)s %(levelname)-7s %(message)s', datefmt='%Y-%d-%m %H:%M:%S', level=logging.DEBUG)

log = logging.getLogger(__name__)
log.info("[System] PyTaranisLogo system is starting up")

# flask imports
try:
    from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, send_from_directory, current_app, jsonify, Markup
except ImportError:
    log.error("[System] Please install flask")
    sys.exit(2)

try:
    from flask.ext.compress import Compress
except ImportError:
    log.error("[System] Please install the flask extension: Flask-Compress")
    sys.exit(2)

# setup flask app
app = Flask(__name__)

# setup logging
# log = app.logger

Compress(app)
app.config['scriptPath'] = os.path.dirname(os.path.realpath(__file__))
app.config['startupDate'] = time.time()

try:
    os.environ['TARANISLOGO_CFG']
    app.logger.info("[System] Loading config from: %s" % os.environ['TARANISLOGO_CFG'])
except KeyError:
    app.logger.warning("[System] Loading config from dist/pytaranislogo.cfg.example becuase TARANISLOGO_CFG environment variable is not set.")
    os.environ['TARANISLOGO_CFG'] = "../dist/pytaranislogo.cfg.example"

try:
    app.config.from_envvar('TARANISLOGO_CFG', silent=False)
except RuntimeError as e:
    app.logger.error(e)
    sys.exit(2)

with app.test_request_context():
    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler(app.config['EMAILSERVER'], app.config['EMAILFROM'], app.config['ADMINS'], current_app.name + ' failed!')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

if not len(app.config['APPSECRET']):
    app.logger.warning("[System] Generating random secret_key. All older cookies will be invalid, but i will NOT work with multiple processes (WSGI).")
    app.secret_key = os.urandom(24)
else:
    app.secret_key = app.config['APPSECRET']

# helpers
def getConfig():
    filePath = os.path.join(app.config['scriptPath'], '..', 'config', 'settings.yml')
    with open(filePath, 'r') as f:
        app.logger.debug("[System] Loading configuration")
        return yaml.load(f)

# flask error handlers
@app.errorhandler(400)
def error_bad_request(error):
    flash("Bad Request", 'error')
    app.logger.warning("[System] 400 Bad Request: %s" % (request.path))
    return redirect(url_for('index'))

@app.errorhandler(401)
def error_unauthorized_request(error):
    flash("Unauthorized request", 'error')
    app.logger.warning("[System] 401 Page not found: %s" % (request.path))
    return redirect(url_for('index'))

@app.errorhandler(403)
def error_forbidden_request(error):
    flash("Forbidden request", 'error')
    app.logger.warning("[System] 403 Page not found: %s" % (request.path))
    return redirect(url_for('index'))

@app.errorhandler(404)
def error_not_found(error):
    flash("Page not found", 'error')
    app.logger.warning("[System] 404 Page not found: %s" % (request.path))
    return redirect(url_for('index'))

@app.errorhandler(500)
def error_internal_server_error(error):
    flash("The server encountered an internal error, probably a bug in the program. The administration was automatically informed of this problem.", 'error')
    app.logger.warning("[System] 500 Internal error: %s" % (request.path))
    return index()

# settings
@app.after_request
def add_header(response):
    response.cache_control.max_age = 2
    response.cache_control.min_fresh = 1
    return response

@app.route('/About')
def about():
    return render_template('about.html')

# support routes
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename=app.config['FAVICON']))

@app.route('/robots.txt')
def get_robots_txt():
    ret = []
    ret.append('User-agent: *')
    ret.append('Allow: /')
    ret.append('Sitemap: %s' % (url_for('get_sitemap_xml', _external=True)))
    return '\n'.join(ret)

@app.route('/sitemap.xml')
def get_sitemap_xml():
    methodsToList = [ 'index', 'about' ]
    ret = []
    ret.append('<?xml version="1.0" encoding="UTF-8"?>')
    ret.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for method in methodsToList:
        ret.append('    <url>')
        ret.append('      <loc>%s</loc>' % (url_for(method, _external=True)))
        ret.append('    </url>')

    ret.append('</urlset>')
    return '\n'.join(ret)

# main route
@app.route('/')
def index():
    cfg = getConfig()

    values = {}
    values['title'] = cfg['texts']['title']['text']
    values['prename'] = cfg['texts']['prename']['text']
    values['surname'] = cfg['texts']['surname']['text']

    return render_template('index.html', values = values)

@app.route('/Render', methods=['POST'])
def image_render():
    def genDlName(title, surname, prename, fileExtension):
        def cleanup(string):
            return string.encode('utf-8').lower().replace(' ', '_')
        return "%s-%s-%s.%s" % (cleanup(title), cleanup(surname), cleanup(prename), fileExtension)

    cfg = getConfig()

    cfg['texts']['title']['text'] = request.form['title']
    cfg['texts']['prename']['text'] = request.form['prename']
    cfg['texts']['surname']['text'] = request.form['surname']
    cfg['defaults']['resourcesPath'] = os.path.join(app.config['scriptPath'], '..', 'resources')
    cfg['defaults']['destinationPath'] = os.path.join(app.config['scriptPath'], 'static', 'output')

    plr = PyTanarisLogo(cfg, app.logger)

    fileName = "%s.%s" % (plr.run(), cfg['defaults']['extension'])
    dlName = genDlName(request.form['title'], request.form['surname'], request.form['prename'], cfg['defaults']['extension'])

    if os.path.isfile(os.path.join(cfg['defaults']['destinationPath'], fileName)):
        return send_from_directory(cfg['defaults']['destinationPath'], fileName, as_attachment = True, attachment_filename = dlName)
    else:
        app.logger.warning("[System] Image not found: %s" % os.path.join(cfg['defaults']['destinationPath'], fileName))
        return redirect(url_for('index'))
