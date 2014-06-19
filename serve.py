import os, os.path, sys
#import json
import subprocess
import select
import logging
from logging import Formatter
from functools import wraps,  update_wrapper

from flask import Flask, request, abort, jsonify, render_template, Response, \
        make_response

from fortunedb import FortuneDB
import random
import flask_auth

app = Flask(__name__)
fortunes = None

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = \
        'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)

@app.route('/fortune/<db>')
@nocache
def get_fortune(db):
    if not db.isalnum():
        abort(400)
    ret = random.choice(fortunes.get(db))
    if request_wants_json():
        return jsonify({'text':ret, 'db': db})
    return render_template('fortune.html', quote=ret)

@app.route('/')
@nocache
def default_fortune():
    if app.config['DEFAULT_FORTUNE'] is not None:
        return get_fortune(app.config['DEFAULT_FORTUNE'])
    abort(404)

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/fortune/<db>/new', methods=['POST'])
@flask_auth.requires_auth
def add(db):
    quote = request.form['quote']
    fortunes.add_quote(db, quote)
    return 'Added'

@app.route('/add/<db>')
def add_ui(db):
    return render_template('add.html', db=db)

if __name__ == '__main__':
    import logging
    #TODO: option for sysloghandler?
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    app.logger.addHandler(handler)
    app.config.from_object('default_config')
    if len(sys.argv) ==  2:
        app.config.from_pyfile(sys.argv[1])
    app.logger.setLevel(logging.DEBUG)
    fortunes = FortuneDB(app.config['FORTUNEPATH'])
    htpass = app.config['HTPASSWD_PATH']
    if htpass is not None and not os.path.exists(htpass):
        print "Htpasswd not found"
        sys.exit(2)
    flask_auth.htpasswd = htpass
    app.run(debug=app.config['DEBUG'])
