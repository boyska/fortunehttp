'''
abstraction (with caching) over fortune db
'''

import os

import comp_fortune

class FortuneDB(object):
    def __init__(self, basedir):
        self.basedir = basedir
        self.cache = {}

    def fetch_fortune(self, name):
        return comp_fortune.read_fortune(os.path.join(self.basedir, name))

    def get(self, name):
        if name not in self.cache or self.cache[name] is None:
            self.cache[name] = list(self.fetch_fortune(name))
        return self.cache[name]

    def flush(self):
        self.cache = {}

    def add_quote(self, name, quote):
        comp_fortune.add_fortune(os.path.join(self.basedir, name), quote,
                verify=True)
        if name in self.cache:
            self.cache[name].append(quote)
