from os import path
from .. import config


def log(message, filename='data/log.txt'):
    fp = open(path.join(config.INSTANCE, filename), 'a')
    fp.write(message+'\n')
    fp.close()
    
