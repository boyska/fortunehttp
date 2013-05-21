import os, os.path, sys
#import json
import subprocess
import select
from logging import Formatter

from flask import Flask, request, abort, jsonify

from fortunedb import FortuneDB
import random

app = Flask(__name__)
fortunes = None


#TODO: make a blueprint
@app.route('/fortune/<db>')
def get_fortune(db):
    if not db.isalnum():
        abort(400)
    ret = random.choice(fortunes.get(db))
    if request_wants_json():
        return jsonify({'text':ret, 'db': db})
    return ret

@app.route('/')
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

if __name__ == '__main__':
    import logging
    #TODO: option for sysloghandler?
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    app.logger.addHandler(handler)
    app.config.from_object('default_config')
    if len(sys.argv) ==  2:
        app.config.from_pyfile(sys.argv[1])
    app.logger.setLevel(logging.DEBUG)
    fortunes = FortuneDB(app.config['FORTUNEPATH'])
    app.run(debug=True)
