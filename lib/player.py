import random, sys, re

class Player:
	def __init__(self, inp=sys.stdin, outp=sys.stdout):
		self.letters = []
		self.score = 0
		self.input = inp
		self.output = outp
		self.turn_pointer = 0
		self.is_passing = False
		self.is_rejected = False
		self.name = None

	def pick_from(self, bag):
		if bag:
			random.shuffle(bag)
			return bag.pop()

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self.pick_from(bag))

	def pass_letters(self):
		self.output.write('\nEnter the letter(s) you want to pass:')
		passed_letters = self.input.readline()[:-1].upper()
		self.passed = list(re.sub('[^A-Z@]', '', passed_letters))

	def make_move(self):
		self.is_passing = False
		self.output.write('\nEnter your move (e.g. h8 r money): ')
		player_input = self.input.readline()[:-1].lower().split()
		if len(player_input) < 3:
			if player_input[0] == 'pass':
				self.is_passing = True
			elif player_input[0] == 'save':
				pass
			else:
				self.output.write('\n==================================================================\n')
				self.output.write('Make sure your input is correct (e.g. h8 r money)'.center(70))
				self.output.write('\n==================================================================\n')
				self.make_move()
		else:
			self.start, self.direction, self.word = player_input
			if self.direction not in ['r', 'd']:
				self.output.write('\n==================================================================\n')
				self.output.write("Your direction should be either 'r' for right or 'd' for down...".center(70))
				self.output.write('\n==================================================================\n')
				self.make_move()
			else:
				self.word = self.word.upper()

	def __str__(self):
		return '{} has got {} points.'.format(self.name, self.score).center(70)