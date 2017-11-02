# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import re

class Board:
	def __init__(self):
		self.wild_letters_on_board = []
		self._prepare_board()
		self._place_bonus()

	def calculate_bonus(self, word_range):
		bonus = {'word': {}, 'letter': {}}

		for square in word_range:
			if self.board[square] == '2w':
				bonus['word'][square] = 2
			elif self.board[square] == '3w':
				bonus['word'][square] = 3
			elif self.board[square] == '2l':
				bonus['letter'][square] = 2
			elif self.board[square] == '3l':
				bonus['letter'][square] = 3
			elif square == 'h8':
				bonus['word'][square] = 2

		return bonus

	def valid_range(self, word_range, word, direction):
		for i, square in enumerate(word_range):
			if i == 0:
				if direction == 'd':
					if self.occupied(square, 'r', self.up_or_left):
						return False
				else:
					if self.occupied(square, 'd', self.up_or_left):
						return False

			if i == len(word_range) - 1:
				if direction == 'd':
					if self.occupied(square, 'r', self.down_or_right):
						return False
				else:
					if self.occupied(square, 'd', self.down_or_right):
						return False

			if self.board[square] != word[i] and re.fullmatch('[A-Z]', self.board[square]):
				return False

		return True

	def place(self, letters, word_range):
		for letter, square in zip(letters, word_range):
			self.board[square] = letter

	def up_or_left(self, square, direction):
		if direction == 'r':
			return self._square_up(square)
		else:
			return self._square_left(square)

	def down_or_right(self, square, direction):
		if direction == 'r':
			return self._square_down(square)
		else:
			return self._square_right(square)

	def occupied(self, square, direction, func):
		# Find the ascii value of the letter on the square.
		# There might be a bonus identifier on the spot.
		# Just in case we grab the first character.
		# If the square is out of range of the board, '.' is given
		letter_ascii = ord(self.board.get(func(square, direction), '.')[0])

		# Check if letter_ascii is a capital letter
		return letter_ascii in range(65, 91)

	def square_occupied(self, square, direction):
		flag1 = self.occupied(square, direction, self.down_or_right)
		flag2 = self.occupied(square, direction, self.up_or_left)

		return flag1 or flag2

	def square_not_occupied(self, square, direction):
		flag1 = not self.occupied(square, direction, self.up_or_left)
		flag2 = not self.occupied(square, direction, self.down_or_right)

		return flag1 and flag2

	def _square_up(self, square):
		# Number part of a spot increases as it goes up
		if len(square) == 2:
			return square[0] + str(int(square[1]) + 1)
		else:
			return square[0] + str(int(square[1:]) + 1)

	def _square_down(self, square):
		# Number part of a spot decreases as it goes up
		if len(square) == 2:
			return square[0] + str(int(square[1]) - 1)
		else:
			return square[0] + str(int(square[1:]) - 1)

	def _square_left(self, square):
		# Letter part of a spot increases as it goes left
		if len(square) == 2:
			return chr(ord(square[0]) - 1) + square[1]
		else:
			return chr(ord(square[0]) - 1) + square[1:]

	def _square_right(self, square):
		# Letter part of a spot decreases as it goes right
		if len(square) == 2:
			return chr(ord(square[0]) + 1) + square[1]
		else:
			return chr(ord(square[0]) + 1) + square[1:]

	def _prepare_board(self):
		self.board = {}

		for num_part in range(1,16):
			row = []

			for let_part in range(ord('a'), ord('p')):
				self.board[chr(let_part) + str(num_part)] = ' '

	def _place_bonus(self):
		for square in self.board:
			if square in 'a1 a8 a15 h15 o15 h1 o8 o1'.split():
				self.board[square] = '3w'

			if square in 'h8 b2 c3 d4 e5 b14 c13 d12 e11 n2 m3 l4 k5 n14 m13 l12 k11'.split():
				self.board[square] = '2w'

			if square in 'b6 b10 n6 n10 f2 f6 f10 f14 j2 j6 j10 j14'.split():
				self.board[square] = '3l'

			if square in 'a4 a12 c7 c9 d1 d8 d15 g3 g7 g9 g13 h4 h12 o4 o12 m7 m9 l1 l8 l15 i3 i7 i9 i13'.split():
				self.board[square] = '2l'