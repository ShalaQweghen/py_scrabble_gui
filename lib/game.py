import random, time, sys

import helpers as helpers

from bag import Bag
from board import Board
from player import Player
from dic import Dict

class Game:
	def __init__(self, config={}):
		self.board = Board()
		self.bag = Bag()
		self.dict = Dict('./lib/dic/sowpods.txt')
		self.turns = 0
		self.passes = 0
		self.points = 0
		self.words = []
		self.word = None
		self.players_list = []
		self.limit = config.get('limit', False)
		self.streams = config.get('streams', False)
		self.on_network = config.get('network', False)
		self.challenging = config.get('challenge', False)
		self.saved = config.get('saved', False)
		self.players = int(config.get('players'))

	def initialize_game(self):
		if self.saved:
			helpers.load(self)
			self.current_player = self.players_list[self.turns % self.players]
		else:
			for p in range(self.players):
				if self.streams:
					player = Player(self.streams[p][0], self.streams[p][1])
					if p == len(self.streams) - 1:
						self.streams = False
				else:
					player = Player()

				player.output.write('\nWhat is Player {}\'s name?: \n'.format(p + 1))
				player.output.flush()
				player.name = player.input.readline()[:-1].upper()
				player.draw_letters(self.bag)

				self.players_list.append(player)

			if self.limit:
				self.set_time_limit()

			random.shuffle(self.players_list)
			self.current_player = self.players_list[0]
			self.prev_player = self.current_player.name

	def initialize_turn(self):
		if self.word:
			self.words.append(self.word.word)
			self.words.extend(self.word.extra_words)

		self.prev_player = self.current_player.name

		if self.on_network:
			for p in self.players_list:
				self.board.display(p.output)
				self.display_turn_info(p)

			self.current_player = self.players_list[self.turns % self.players]

			for p in self.players_list:
				if p is not self.current_player:
					p.output.write("\nIt's {}'s turn...\n\n".format(self.current_player.name))
					p.output.flush()
		else:
			self.current_player = self.players_list[self.turns % self.players]
			self.board.display(self.current_player.output)
			self.display_turn_info(self.current_player)

		self.turns += 1
		self.words = []

	def display_turn_info(self, p):
		p.output.write(
			"\n\033[1mPlayer:\033[0m {}\t\t\033[1m|\033[0m  \033[1mTotal Points:\033[0m {}\n".format(
				p.name, p.score
			)
		)
		p.output.write(
			"\033[1mLetters Left in Bag:\033[0m {}\t\033[1m|\033[0m  \033[1mWords:\033[0m {} for {} pts by {}\n\n".format(
				len(self.bag.bag), self.words, self.points, self.prev_player
			)
		)
		p.output.write("\u2551 {} \u2551\n".format(' - '.join(p.letters)).center(70))
		p.output.flush()

	def play_turn(self):
		self.current_player.get_move(self.bag, self.board, self.dict)

		while self.current_player.is_saving:
			helpers.save(self)
			self.current_player.get_move(self.bag, self.board, self.dict)

		self.word = self.current_player.word

		if self.current_player.is_passing:
			self.passes += 1
		elif self.move_acceptable() and self.word.valid():
			self.points = self.word.points

			if self.turns == 1:
				self.points += self.word.points

			self.board.place(self.word.word, self.word.range)
			self.current_player.update_rack(self.bag)

			if self.current_player.full_bonus:
				self.points += 60

			self.current_player.update_score(self.points)
			self.passes = 0
		else:
				self.current_player.display_message(self.word.error_message)
				if self.word.invalid_word:
					self.handle_invalid_word()
				else:
					self.play_turn()

	def move_acceptable(self):
		if self.limit and self.time_over():
			self.end_game()

		return True

	def handle_invalid_word(self):
		if not self.challenging:
			self.play_turn()
		else:
			self.passes += 1
			self.points = 0
			self.word.reset()

	def set_time_limit(self):
		start_time = time.time()
		self.end_time = start_time + int(self.limit) * 60

	def time_over(self):
		return time.time() >= self.end_time

	def decide_winner(self):
		winner = self.current_player

		for p in self.players_list:
			if p.score > winner.score:
				winner = p

		return winner

	def end_game(self):
		winner = self.decide_winner()

		for p in ((self.on_network and self.players_list) or [self.current_player]):
			p.output.write('\n==================================================================\n\n')
			if self.limit and self.time_over():
				p.output.write('TIME IS UP!\n'.center(70))
			else:
				p.output.write('GAME IS OVER!\n'.center(70))

			p.output.write('\n')
			p.output.write('The winner is \033[1m{}\033[0m with \033[1m{}\033[0m points!\n'.format(winner.name, winner.score).center(85))
			p.output.write('\n==================================================================\n')

		sys.exit()

	def enter_game_loop(self):
		try:
			self.initialize_game()
			while len(self.bag.bag) > 0 and self.passes != 3 * self.players:
				try:
					self.initialize_turn()
					self.play_turn()
				except KeyboardInterrupt:
					answer = input('\nAre you sure about cancelling the game (y/n) ?: ').upper()[0]
					if answer == 'Y':
						sys.exit()
					else:
						self.turns -= 1
			self.end_game()
		except BrokenPipeError:
				for p in self.players_list:
					try:
						p.output.write('\nA player has quit the game. The game is cancelled.\n\n')
						p.output.flush()
					except:
						continue
