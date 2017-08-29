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
		self.players = config.get('players')
		self.letter_points = helpers.set_letter_points()

	def initialize_game(self):
		if self.saved:
			helpers.load(self)
		else:
			for p in range(self.players):
				if self.streams:
					player = Player(self.streams[p][0], self.streams[p][1])
					if p == len(self.streams) - 1:
						self.streams = False
				else:
					player = Player()

				player.output.write('What is Player {}\'s name?: \n'.format(p + 1))
				player.output.flush()
				player.name = player.input.readline()[:-1].upper()
				player.draw_letters(self.bag)

				self.players_list.append(player)

			if self.limit:
				self.set_time_limit()

			random.shuffle(self.players_list)
			self.current_player = self.players_list[0]

	def initialize_turn(self):
		if self.word:
			self.words.append(self.word.word)
			self.words.extend(self.word.extra_words)

		if self.on_network:
			for p in self.players_list:
				self.board.display(p.output)
				self.display_turn_info(p)
			self.current_player = self.players_list[self.turns % self.players]
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
				len(self.bag.bag), self.words, self.points, self.current_player.name
			)
		)
		p.output.write("\t\t   \u2551 {} \u2551\n\n".format(' - '.join(p.letters)))
		p.output.flush()

	def play_turn(self):
		self.current_player.get_move(self.bag, self.board, self.dict)

		while self.current_player.is_saving:
			helpers.save(self)
			self.current_player.get_move(self.bag, self.board, self.dict)

		self.word = self.current_player.word

		if self.current_player.is_passing:
			self.passes += 1
		elif self.dict.valid_word(self.word.word):
			if self.valid_move() and self.word.process_extra_words():
				self.calculate_points()
				self.board.place(self.word.word, self.word.range)
				self.current_player.update_rack(self.bag)
				self.passes = 0
			else:
				if not self.valid_move():
					self.current_player.display_message('Move was illegal...\n')
					self.play_turn()
				else:
					self.current_player.display_message('{} is not in the dictionary...\n'.format(self.word.invalid_word))
					self.handle_invalid_word()
		else:
			self.current_player.display_message('{} is not in dictionary...\n'.format(self.word.word))
			self.handle_invalid_word()

	def valid_move(self):
		if self.limit and self.time_over():
			self.end_game()

		if len(self.bag.bag) == 100 - 7 * self.players:
			return self.word.start == 'h8'

		for square in self.word.range:
			if self.word.aob_list:
				return True
			elif self.board.square_occupied(square, self.word.direction):
				return True

		return False

	def calculate_points(self):
		bonus = self.board.calculate_bonus(self.word.range)
		word_bonus = bonus.get('word', None)
		letter_bonus = bonus.get('letter', None)

		word_points = 0
		self.points = 0

		for l, s in zip(self.word.word, self.word.range):
			if letter_bonus:
				word_points += (letter_bonus.get(s, 0) + 1) * self.letter_points[l]
			else:
				word_points += self.letter_points[l]

		if word_bonus:
			for s in self.word.range:
				self.points += word_bonus.get(s, 0) * word_points
		else:
			self.points += word_points

		for w in self.word.extra_words:
			word_points = 0
			for l in w:
				word_points += self.letter_points[l]
			self.points += word_points

		for s, l in self.word.extra_spots:
			if letter_bonus:
				self.points += letter_bonus.get(s, 0) * self.letter_points[l]

		self.current_player.update_score(self.points)

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
			p.output.write('\n==================================================================\n')
			if self.time_over():
				p.output.write('TIME IS UP!\n'.center(70))
			else:
				p.output.write('GAME IS OVER!\n'.center(70))
			p.output.write('The winner is \033[1m{}\033[0m with \033[1m{}\033[0m points!'.format(winner.name, winner.score).center(70))
			p.output.write('\n==================================================================\n')

		sys.exit()

	def enter_game_loop(self):
		self.initialize_game()
		while len(self.bag.bag) > 0 and self.passes != 3 * self.players:
			self.initialize_turn()
			try:
				self.play_turn()
			except KeyboardInterrupt:
				answer = input('Are you sure about cancelling the game (y/n) ?: ').upper()[0]
				if answer == 'Y':
					sys.exit()
				else:
					self.turns -= 1
		self.end_game()
