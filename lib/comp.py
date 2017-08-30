import sys, itertools
from word import Word

class AIOpponent():
  def __init__(self):
    self.word = None
    self.letters = []
    self.score = 0
    self.input = sys.stdin
    self.output = sys.stdout
    self.is_passing = False
    self.is_saving = False
    self.full_bonus = False
    self.wild_tile = None
    self.name = 'COMP'

  def draw_letters(self, bag, amount=7):
    for i in range(amount):
      self.letters.append(self._pick_from(bag))

  def update_rack(self, bag):
    aob = len(self.word.aob_list)

    for l in self.word.word:
      self._remove_tile(l)

    if len(self.letters) == 0:
      self.full_bonus = True

    self.draw_letters(bag, len(self.word.word) - aob)

  def update_score(self, points):
    self.score += points

  def get_move(self, bag, board, dic):
    self.full_bonus = False

    if '@' in self.letters:
      self.letters[self.letters.index('@')] = 'S'

    words = []
    word_set = set()
    for n in range(2, len(self.letters) + 1):
      word_set = word_set.union(self._permute(n, dic))

    for word in word_set:
      for key in board.board.keys():
        word_d = Word(key, 'd', word, board, dic)
        word_r = Word(key, 'r', word, board, dic)

        if word_d.valid():
          words.append(word_d)

        if word_r.valid():
          words.append(word_r)

    self.word = words[0]

    for word in words:
      if word.calculate_points() > self.word.calculate_points():
        self.word = word

  def _permute(self, n, dic):
    words = set()
    perms = itertools.permutations(self.letters, n)

    for perm in perms:
      if dic.valid_word(''.join(perm)):
        words.add(''.join(perm))

    return words

  def _pick_from(self, bag):
    if bag:
      return bag.draw()

  def _remove_tile(self, l):
    if l in self.word.aob_list:
      self.word.aob_list.remove(l)
    elif l not in self.word.aob_list:
      self.letters.remove(l)




