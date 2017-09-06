from tkinter import *

class Tile(Label):
  def __init__(self, parent=None, letter=''):
    self.var = StringVar()
    self.var.set(letter)
    self.letter = None

    Label.__init__(self, parent, textvariable=self.var)
    self.config(bd=1, bg='#E9BE99',height=2, width=4, relief=SUNKEN)

class BoardTile(Tile):
  def __init__(self, row, col, parent=None, letter=''):
    Tile.__init__(self, parent, letter)
    self.grid(row=row, column=col, sticky=W+E+N+S)

    self.name = None
    self.active = True

class RackTile(Tile):
  def __init__(self, parent=None, letter=''):
    Tile.__init__(self, parent, letter)
    self.pack(side=LEFT)
