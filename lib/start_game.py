import sys

from interface import Interface

config = {}

if '-d' in sys.argv:
  config['save_meaning'] = True

Interface(config)