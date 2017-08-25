import sys, re

class Player:
	def __init__(self, inp=sys.stdin, outp=sys.stdout, name=None):
		self.letters = []
		self.score = 0
		self.input = inp
		self.output = outp
		self.turn_pointer = 0
		self.is_passing = False
		self.is_rejected = False
		self.name = name

	def _pick_from(self, bag):
		if bag:
			return bag.draw()

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self._pick_from(bag))

	def pass_letters(self, bag):
		self.output.write('\nEnter the letter(s) you want to pass:')
		player_input = self.input.readline()[:-1].upper()
		passed_letters = list(re.sub('[^A-Z@]', '', player_input))

		for l in passed_letters:
			self.letters.remove(l)

		bag.put_back(passed_letters)
		self.draw_letters(bag, len(passed_letters))

	def update_letters(self, bag):
		for l in self.word:
			self.letters.remove(l)

		self.draw_letters(bag, len(self.word))

	def get_move(self, bag):
		self.is_passing = False
		self.output.write('\nEnter your move (e.g. h8 r money): ')
		player_input = self.input.readline()[:-1].lower().split()

		if len(player_input) < 3:
			if player_input[0] == 'pass':
				self.is_passing = True
				self.pass_letters(bag)
			elif player_input[0] == 'save':
				pass
			else:
				self.output.write('\n==================================================================\n')
				self.output.write('Make sure your input is correct (e.g. h8 r money)'.center(70))
				self.output.write('\n==================================================================\n')
				self.get_move(bag)
		else:
			self.start, self.direction, self.word = player_input

			if self.direction not in ['r', 'd']:
				self.output.write('\n==================================================================\n')
				self.output.write("Your direction should be either 'r' for right or 'd' for down...".center(70))
				self.output.write('\n==================================================================\n')
				self.get_move(bag)
			else:
				self.word = self.word.upper()

	def __str__(self):
		return '{} has got {} points.'.format(self.name, self.score).center(70)