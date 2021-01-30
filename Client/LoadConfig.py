import ujson
import os


class NetworkConfig(object):
    def __init__(self, base_dir):
        self.config = open(os.path.join(base_dir, 'Network.json'), 'r', encoding='utf8').read()
        self.config = ujson.loads(self.config)

    def get(self, key):
        return self.config.get(key)
