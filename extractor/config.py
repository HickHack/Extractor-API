import os
from configparser import RawConfigParser


class Config(object):

    def __init__(self):
        self.path = ('%s/config.properties' % os.path.split(os.path.abspath(__file__))[0])
        self.config = RawConfigParser()

        self.load()

    def load(self):
        if os.access(self.path, os.F_OK) and os.path.isfile(self.path):
            self.config.read(self.path)

    def linkedIn(self):
        return self.config['LINKEDIN']

    def neo4j(self):
        return self.config['NEO4J']

    def env(self):
        return self.config['ENV']


