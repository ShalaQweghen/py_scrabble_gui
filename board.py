class Board:

	def __init__(self):
		self.prepare_board()
		self.place_bonus()

	def prepare_board(self):
		self.board = {}
		self.rows = []
		for i in range(1,16):
			row = []
			for l in range(ord('a'), ord('p')):
				self.board[chr(l) + str(i)] = ' '
				row.append(chr(l) + str(i))
			self.rows.append(row)

	def place_bonus(self):
		for key in self.board:
			if key in ['a1','a8','a15','h15','o15','h1','o8','o1']:
				self.board[key] = '3w'
			if key in ['b2','c3','d4','e5','b14','c13','d12','e11','n2','m3','l4','k5','n14','m13','l12','k11']:
				self.board[key] = '2w'
			if key in ['b6','b10','n6','n10','f2','f6','f10','f14','j2','j6','j10','j14']:
				self.board[key] = '3l'
			if key in ['a4','a12','c7','c9','d1','d8','d15','g3','g7','g9','g13','h4','h12','o4','o12','m7','m9','l1','l8','l15','i3','i7','i9','i13']:
				self.board[key] = '2l'

	def display(self):
		t_line = u'\u2550\u2550\u2550\u2566'
		m_line = u'\u2550\u2550\u2550\u256C'
		b_line = u'\u2550\u2550\u2550\u2569'
		hor = u'\u2551'
		ver = u'\u2550'
		lcu = u'\u2554'
		rcu = u'\u2557'
		lcm = u'\u2560'
		rcm = u'\u2563'
		lcd = u'\u255A'
		rcd = u'\u255D'
		row_number = 15
		print("\n     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o")
		print("   {0}".format(lcu + t_line * 14 + ver * 3 + rcu))
		for row in self.rows:
			if row_number < 10:
				print("{}  ".format(row_number), end="")
			else:
				print("{} ".format(row_number), end="")
			for spot in row:
				if self.board[spot] == "3w":
					print("{}\x1b[31m{} \x1b[00m".format(hor, self.board[spot]), end="")
				elif self.board[spot] == "2w":
					print("{}\x1b[35m{} \x1b[00m".format(hor, self.board[spot]), end="")
				elif self.board[spot] == "3l":
					print("{}\x1b[34m{} \x1b[00m".format(hor, self.board[spot]), end="")
				elif self.board[spot] == "2l":
					print("{}\x1b[36m{} \x1b[00m".format(hor, self.board[spot]), end="")
				else:
					print("{}\033[1m {} \033[0m".format(hor, self.board[spot]), end="")
			print("{} {}".format(hor, row_number))
			row_number -= 1
			if row_number > 0:
				print("   {0}".format(lcm + m_line * 14 + ver * 3 + rcm))
			else:
				print("   {0}".format(lcd + b_line * 14 + ver * 3 + rcd))
		print("     a   b   c   d   e   f   g   h   i   j   k   l   m   n   o")