from bag import Bag
from board import Board
from player import Player

class Game:
	def __init__(self, config={}):
		self.board = Board()
		self.bag = Bag()
		self.dic = open('dic/sowpods.txt').read().splitlines()
		self.non_discard = []
		self.word_list = []
		self.turns = 1
		self.passes = 0
		self.points = []
		self.names = config.get('names', {})
		self.limit = config.get('limit')
		self.streams = config.get('streams')
		self.on_network = config.get('network')
		self.challenging = config.get('challenge')
		self.saved = config.get('saved')
		self.players = len(config['streams']) if self.on_network else 2
		self.bold_on = '\033[1m'
		self.bold_off = '\033[0m'