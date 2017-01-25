import os
from configparser import ConfigParser


class Config(object):

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(os.path.split(os.path.abspath(__file__))[0]+'/config.properties')

    def linkedIn(self):
        return self.config['LINKEDIN']

    def neo4j(self):
        return self.config['NEO4J']



