import re

class Board:
	def __init__(self):
		self.wild_tiles_on_board = []
		self._prepare_board()
		self._place_bonus()

	def display(self, output):
		# Components of the board outline
		t_line = u'\u2550\u2550\u2550\u2566'
		m_line = u'\u2550\u2550\u2550\u256C'
		b_line = u'\u2550\u2550\u2550\u2569'
		hor, ver = u'\u2551', u'\u2550'
		lcu, rcu = u'\u2554', u'\u2557'
		lcm, rcm = u'\u2560', u'\u2563'
		lcd, rcd = u'\u255A', u'\u255D'

		row_number = 15

		output.write('\n     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o\n')
		output.write('   {}\n'.format(lcu + t_line * 14 + ver * 3 + rcu))

		for row in self.rows:
			if row_number < 10:
				output.write('{}  '.format(row_number))
			else:
				output.write('{} '.format(row_number))

			for spot in row:
				if self.board[spot] == '3w':
					output.write('{}\x1b[31m{} \x1b[00m'.format(hor, self.board[spot]))
				elif self.board[spot] == '2w':
					output.write('{}\x1b[35m{} \x1b[00m'.format(hor, self.board[spot]))
				elif self.board[spot] == '3l':
					output.write('{}\x1b[34m{} \x1b[00m'.format(hor, self.board[spot]))
				elif self.board[spot] == '2l':
					output.write('{}\x1b[36m{} \x1b[00m'.format(hor, self.board[spot]))
				else:
					output.write('{}\033[1m {} \033[0m'.format(hor, self.board[spot]))

			output.write('{} {}\n'.format(hor, row_number))

			row_number -= 1

			if row_number > 0:
				output.write('   {}\n'.format(lcm + m_line * 14 + ver * 3 + rcm))
			else:
				output.write('   {}\n'.format(lcd + b_line * 14 + ver * 3 + rcd))

		output.write('     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o\n')

		output.flush()

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
		for i, s in enumerate(word_range):
			if i == 0:
				if direction == 'd':
					if self.occupied(s, 'r', self.up_or_left):
						return False
				else:
					if self.occupied(s, 'd', self.up_or_left):
						return False

			if i == len(word_range) - 1:
				if direction == 'd':
					if self.occupied(s, 'r', self.down_or_right):
						return False
				else:
					if self.occupied(s, 'd', self.down_or_right):
						return False

			if self.board[s] != word[i] and re.fullmatch('[A-Z]', self.board[s]):
				return False

		return True

	def place(self, letters, word_range):
		for l, s in zip(letters, word_range):
			self.board[s] = l

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
		return ord(self.board.get(func(square, direction), ['.'])[0]) in range(65, 91)

	def square_occupied(self, square, direction):
		return self.occupied(square, direction, self.up_or_left) or self.occupied(square, direction, self.down_or_right)

	def square_not_occupied(self, square, direction):
		return not self.occupied(square, direction, self.up_or_left) and not self.occupied(square, direction, self.down_or_right)

	def _square_up(self, square):
		if len(square) == 2:
			return square[0] + str(int(square[1]) + 1)
		else:
			return square[0] + str(int(square[1:]) + 1)

	def _square_down(self, square):
		if len(square) == 2:
			return square[0] + str(int(square[1]) - 1)
		else:
			return square[0] + str(int(square[1:]) - 1)

	def _square_left(self, square):
		if len(square) == 2:
			return chr(ord(square[0]) - 1) + square[1]
		else:
			return chr(ord(square[0]) - 1) + square[1:]

	def _square_right(self, square):
		if len(square) == 2:
			return chr(ord(square[0]) + 1) + square[1]
		else:
			return chr(ord(square[0]) + 1) + square[1:]

	def _prepare_board(self):
		self.board = {}
		self.rows = []

		for i in range(1,16):
			row = []

			for l in range(ord('a'), ord('p')):
				self.board[chr(l) + str(i)] = ' '
				row.append(chr(l) + str(i))

			self.rows.append(row)

		self.rows.reverse()

	def _place_bonus(self):
		for key in self.board:
			if key in 'a1 a8 a15 h15 o15 h1 o8 o1'.split():
				self.board[key] = '3w'

			if key in 'h8 b2 c3 d4 e5 b14 c13 d12 e11 n2 m3 l4 k5 n14 m13 l12 k11'.split():
				self.board[key] = '2w'

			if key in 'b6 b10 n6 n10 f2 f6 f10 f14 j2 j6 j10 j14'.split():
				self.board[key] = '3l'

			if key in 'a4 a12 c7 c9 d1 d8 d15 g3 g7 g9 g13 h4 h12 o4 o12 m7 m9 l1 l8 l15 i3 i7 i9 i13'.split():
				self.board[key] = '2l'