# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import re

from lib.word import Word

class Player:
	def __init__(self, name=None):
		self.name = name
		self.score = 0
		self.letters = []
		self.wild_letters = []
		self.word = None
		self.full_bonus = False
		self.passed_letters = []
		self.new_letters = []

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self._pick_from(bag))

			# $ means there are no letters left in the bag
			if self.letters[-1] != '$':
				self.new_letters.append(self.letters[-1])

		self.letters = list(re.sub('[^A-Z@]', '', ''.join(self.letters)))

	def update_rack(self, bag):
		self.new_letters = []

		if self.passed_letters:
			for letter in self.passed_letters:
				if letter in self.letters:
					self._remove_tile(letter)
		else:
			aob = len(self.word.aob_list)

			for letter in self.word.word:
				self._remove_tile(letter)

			if len(self.letters) == 0 and len(bag.bag) != 0:
				self.full_bonus = True

		if len(bag.bag) > 0:
			if self.passed_letters:
				self.draw_letters(bag, 7 - len(self.letters))
			else:
				self.draw_letters(bag, len(self.word.word) - aob)

		self.passed_letters = []

	def update_score(self, points=0):
		# If a points argument provided, it means
		# that it should be substracted
		if points:
			self.score -= points
		else:
			self.score += self.word.calculate_total_points()

			if self.full_bonus:
				self.score += 60

	def _pick_from(self, bag):
		if bag:
			return bag.draw()

	def _remove_tile(self, letter):
		if letter not in self.wild_letters:
			if self.passed_letters and letter in self.letters:
				self.letters.remove(letter)
			elif letter in self.word.aob_list:
				self.word.aob_list.remove(letter)
			else:
				self.letters.remove(letter)
		else:
			self.letters.remove('@')
			self.wild_letters.remove(letter)