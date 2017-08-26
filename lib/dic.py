class Dict:
  def __init__(self, dic):
    self.dict = open(dic).read().splitlines()

  def valid_word(self, word):
    return word in self.dict