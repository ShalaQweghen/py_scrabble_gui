# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

class Dict:
  def __init__(self, dic):
    self.dict = open(dic).read().splitlines()

  def valid_word(self, word):
    return word in self.dict