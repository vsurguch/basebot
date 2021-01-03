from os import path

def log(message, filename='data/log.txt'):
    fp = open(path.join(path.dirname(__file__), filename), 'a')
    fp.write(message+'\n')
    fp.close()
    
