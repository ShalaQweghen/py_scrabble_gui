import sys

from lib.interface import Interface

config = {}

if '-d' in sys.argv:
  config['save_meaning'] = True

Interface(config)