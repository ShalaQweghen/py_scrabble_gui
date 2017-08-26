import sys, re

class Player:
	def __init__(self, inp=sys.stdin, outp=sys.stdout, name=None):
		self.letters = []
		self.score = 0
		self.input = inp
		self.output = outp
		self.wild_tile = None
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
		self.output.write('\nEnter the letter(s) you want to pass: ')
		player_input = self.input.readline()[:-1].upper()
		passed_letters = list(re.sub('[^A-Z@]', '', player_input))

		if self._letters_on_rack(passed_letters):
			for l in passed_letters:
				self.letters.remove(l)

			bag.put_back(passed_letters)
			self.draw_letters(bag, len(passed_letters))
		else:
			self.output.write('\n==================================================================\n')
			self.output.write("One or more letters are not on your rack...".center(70))
			self.output.write('\n==================================================================\n')
			self.get_move(bag)


	def replace_wild_tile(self, output):
		output.write("What letter will you use the wild tile for? ")
		self.wild_tile = self.input.readline()[:-1].upper()
		self.word = re.sub('@', self.wild_tile, self.word)

	def update_rack(self, bag):
		if self.wild_tile:
			self.letters[self.letters.index('@')] = self.wild_tile

		for l in self.word:
			self.letters.remove(l)

		self.draw_letters(bag, len(self.word))

	def _letters_on_rack(self, word):
		if '@' in word:
			self.replace_wild_tile(self.output)

		if self.wild_tile:
			self.letters[self.letters.index('@')] = self.wild_tile

		for l in word:
			if l not in self.letters or word.count(l) > self.letters.count(l):
				return False

		if self.wild_tile:
			self.letters[self.letters.index(self.wild_tile)] = '@'

		return True

	def get_move(self, bag):
		self.wild_tile = None
		self.is_passing = False

		self.output.write('\nEnter your move (e.g. h8 r money): ')
		player_input = self.input.readline()[:-1].lower().split()

		if len(player_input) < 3 or len(player_input) > 3:
			if player_input[0] == 'pass':
				self.pass_letters(bag)
				self.is_passing = True
			elif player_input[0] == 'save':
				pass
			else:
				self.output.write('\n==================================================================\n')
				self.output.write('Make sure your input is correct (e.g. h8 r money)'.center(70))
				self.output.write('\n==================================================================\n')
				self.get_move(bag)
		else:
			self.start, self.direction, self.word = player_input
			self.word = self.word.upper()

			if self.direction not in ['r', 'd']:
				self.output.write('\n==================================================================\n')
				self.output.write("Your direction should be either 'r' for right or 'd' for down...".center(70))
				self.output.write('\n==================================================================\n')
				self.get_move(bag)
			elif not self._letters_on_rack(self.word):
				self.output.write('\n==================================================================\n')
				self.output.write("One or more letters are not on your rack...".center(70))
				self.output.write('\n==================================================================\n')
				self.get_move(bag)

	def __str__(self):
		return '{} has got {} points.'.format(self.name, self.score).center(70)