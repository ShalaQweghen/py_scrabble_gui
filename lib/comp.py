# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import itertools, random

from lib.word import Word
from lib.player import Player

class AIOpponent(Player):
  def get_move(self, bag, board, dic):
    self.wild_letters = []
    self.full_bonus = False
    self.is_passing = False

    # Change all wild tiles to letter S
    if '@' in self.letters:
      for i in range(self.letters.count('@')):
        self.letters[self.letters.index('@')] = 'S'
        self.wild_letters.append('S')

    words = []
    word_set = set()

    # All the possible valid permutations of the letters
    for n in range(2, len(self.letters) + 1):
      word_set = word_set.union(self._permute(n, dic))

    # Check if the word can be played validly horizontally or vertically
    for word in word_set:
      for spot in board.board.keys():
        word_d = Word(spot, 'd', word, board, dic)
        word_r = Word(spot, 'r', word, board, dic)

        if word_d.validate():
          words.append(word_d)

        if word_r.validate():
          words.append(word_r)

    if len(words) == 0:
      self.is_passing = True
      self._pass_letters(bag)
    else:
      self.word = words[0]

      # Add wild tile S to word wild tile list so that it doesn't get points
      for i in range(len(self.wild_letters)):
        if 'S' in self.word.word:
          self.word.wild_letters.append(self.word.range[self.word.word.index('S')])

      for word in words:
        # Add wild tile S to word wild tile list so that it doesn't get points
        for i in range(len(self.wild_letters)):
          if 'S' in word.word:
            word.wild_letters.append(word.range[word.word.index('S')])

        # Pick the word with more points
        if word.calculate_total_points() > self.word.calculate_total_points():
          self.word = word

      # Put back the wild letter character in the letters array
      for letter in self.wild_letters:
        self.letters[self.letters.index('S')] = '@'

      return self.word

  def _permute(self, n, dic):
    words = set()
    perms = itertools.permutations(self.letters, n)

    for perm in perms:
      if dic.valid_word(''.join(perm)):
        words.add(''.join(perm))

    return words

  def _pass_letters(self, bag):
    # Randomly pass three letters
    passed_letters = random.sample(self.letters, 3)

    for l in passed_letters:
      self.letters.remove(l)

    bag.put_back(passed_letters)
    self.draw_letters(bag, len(passed_letters))