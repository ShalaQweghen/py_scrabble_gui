import random

from bag import Bag
from board import Board
from player import Player
from dic import Dict
from word import Word
from scrabble.valid_move_helpers import *
from scrabble.extra_word import *

class Game:
	def __init__(self, config={}):
		self.board = Board()
		self.bag = Bag()
		self.dict = Dict('./lib/dic/sowpods.txt')
		self.non_discard = []
		self.word_list = []
		self.turns = 0
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

	def initialize_players(self):
		for p in range(self.players):
			player = Player(name=input("What is Player's name? "))
			player.draw_letters(self.bag)
			self.players_list.append(player)

		random.shuffle(self.players_list)

	def initialize_turn(self):
		self.current_player = self.players_list[self.turns % self.players]
		self.turns += 1
		self.word_list = []
		self.board.display()

	def display_turn_info(self):
		self.current_player.output.write(
			"\n\033[1mPlayer:\033[0m {}\t\t\033[1m|\033[0m  \033[1mTotal Points:\033[0m {}\n".format(
				self.current_player.name, self.current_player.score
			)
		)
		self.current_player.output.write(
			"\033[1mLetters Left in Bag:\033[0m {}\t\033[1m|\033[0m  \033[1mWords Prev. Made:\033[0m {} for {} points\n\n".format(
				len(self.bag.bag), [], 0
			)
		)
		self.current_player.output.write("\t\t   \u2551 {} \u2551\n".format(' - '.join(self.current_player.letters)))

	def play_turn(self):
		self.current_player.get_move(self.bag)
		self.word = self.current_player.word
		self.word.board = self.board.board

		if self.current_player.is_passing:
			self.passes += 1
		elif self.dict.valid_word(self.word.word):
			if self.valid_move() and check_extra_word(self.word, self.word_list, self.dict):
				self.board.place(self.word.word, self.word.range)
				self.current_player.update_rack(self.bag)
				self.passes = 0
			else:
				self.current_player.output.write('\n==================================================================\n')
				self.current_player.output.write('Move was illegal...'.center(70))
				self.current_player.output.write('\n==================================================================\n')
				self.play_turn()
		else:
			self.current_player.output.write('\n==================================================================\n')
			self.current_player.output.write('Word is not in dictionary...'.center(70))
			self.current_player.output.write('\n==================================================================\n')
			self.play_turn()

	def valid_move(self):
		if len(self.bag.bag) == 100 - 7 * self.players:
			return self.word.start == 'h8'

		for square in self.word.range:
			if occupied_up_or_left(square, self.word):
				return True
			elif occupied_down_or_right(square, self.word):
				return True

		return False

	def enter_game_loop(self):
		self.initialize_players()
		while len(self.bag.bag) > 0 and self.passes != 3 * self.players:
			self.initialize_turn()
			self.display_turn_info()
			self.play_turn()







g = Game()
g.enter_game_loop()