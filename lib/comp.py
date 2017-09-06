import sys, itertools, random

from lib.word import Word
from lib.player import Player

class AIOpponent(Player):
  def get_move(self, bag, board, dic):
    self.wild_tiles = []
    self.full_bonus = False
    self.is_passing = False

    if '@' in self.letters:
      for i in range(self.letters.count('@')):
        self.letters[self.letters.index('@')] = 'S'
        self.wild_tiles.append('S')

    words = []
    word_set = set()

    for n in range(2, len(self.letters) + 1):
      word_set = word_set.union(self._permute(n, dic))

    for word in word_set:
      for key in board.board.keys():
        word_d = Word(key, 'd', word, board, dic)
        word_r = Word(key, 'r', word, board, dic)

        if word_d.validate():
          words.append(word_d)

        if word_r.validate():
          words.append(word_r)

    if len(words) == 0:
      self.is_passing = True
      self._pass_letters(bag)
    else:
      self.word = words[0]

      for i in range(len(self.wild_tiles)):
        if 'S' in self.word.word:
          self.word.wild_tiles.append(self.word.range[self.word.word.index('S')])

      for word in words:
        for i in range(len(self.wild_tiles)):
          if 'S' in word.word:
            word.wild_tiles.append(word.range[word.word.index('S')])

        if word.calculate_total_points() > self.word.calculate_total_points():
          self.word = word

      return self.word

  def _permute(self, n, dic):
    words = set()
    perms = itertools.permutations(self.letters, n)

    for perm in perms:
      if dic.valid_word(''.join(perm)):
        words.add(''.join(perm))

    return words

  def _pass_letters(self, bag):
    passed_letters = random.sample(self.letters, 3)
    for l in passed_letters:
      self.letters.remove(l)

    bag.put_back(passed_letters)
    self.draw_letters(bag, len(passed_letters))



