from bag import Bag
from board import Board
from player import Player
from scrabble.letter_word import *

class Game:
	def __init__(self, config={}):
		self.board = Board()
		self.bag = Bag().bag
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
		self.players_list = []
		self.bold_on = '\033[1m'
		self.bold_off = '\033[0m'

	def initialize_players(self):
		for p in range(self.players):
			player = Player(name=input("What is Player's Name?"))
			self.players_list.append(player)

		for p in self.players_list:
			p.draw_letters(self.bag)
			print(p.name)
			print(p.letters)
			p.make_move()
			print(p.word)


Game().initialize_players()