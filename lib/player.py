import sys, re
from lib.word import Word

class Player:
	def __init__(self, name=None):
		self.name = name
		self.score = 0
		self.letters = []
		self.wild_tiles = []
		self.word = None
		self.full_bonus = False
		self.passed_letters = []
		self.new_letters = []

	def set_passed_letters(self, passed_letters):
		self.passed_letters = passed_letters

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self._pick_from(bag))
			if self.letters[-1] != '$':
				self.new_letters.append(self.letters[-1])

		self.letters = list(re.sub('[^A-Z@]', '', ''.join(self.letters)))

	def update_rack(self, bag):
		self.new_letters = []

		if not self.passed_letters:
			aob = len(self.word.aob_list)

		if self.passed_letters:
			for l in self.passed_letters:
				if l in self.letters:
					self._remove_tile(l)
		else:
			for l in self.word.word:
				self._remove_tile(l)

		if not self.passed_letters and len(self.letters) == 0:
			self.full_bonus = True

		if len(bag.bag) > 0:
			if self.passed_letters:
				self.draw_letters(bag, 7 - len(self.letters))
			else:
				self.draw_letters(bag, len(self.word.word) - aob)

		self.passed_letters = []

	def update_score(self, points=0):
		if points:
			self.score -= points
		else:
			self.score += self.word.calculate_total_points()

			if self.full_bonus:
				self.score += 60

	def _pick_from(self, bag):
		if bag:
			return bag.draw()

	def _remove_tile(self, l):
		if l not in self.wild_tiles:
			if self.passed_letters and l in self.letters:
				self.letters.remove(l)
			elif l in self.word.aob_list:
				self.word.aob_list.remove(l)
			else:
				self.letters.remove(l)
		else:
			self.letters.remove('@')
			self.wild_tiles.remove(l)