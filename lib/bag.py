# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import random

class Bag:
	def __init__(self):
		self.bag = []
		self._fill_bag()

	def _fill_bag(self):
		self.bag.extend(['Q','Z','J','X','K'])
		for i in range(2): self.bag.extend(['F','H','V','W','Y','B','C','M','P','@'])
		for i in range(3): self.bag.extend(['G'])
		for i in range(4): self.bag.extend(['D','U','S','L'])
		for i in range(6): self.bag.extend(['T','R','N'])
		for i in range(8): self.bag.extend(['O'])
		for i in range(9): self.bag.extend(['I','A'])
		for i in range(12): self.bag.extend(['E'])

	def draw(self):
		random.shuffle(self.bag)
		try:
			return self.bag.pop()
		except IndexError:
			return '$'

	def put_back(self, letters):
		self.bag.extend(letters)