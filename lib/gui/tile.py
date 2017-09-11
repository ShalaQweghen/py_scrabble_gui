from tkinter import *

class Tile(Label):
  def __init__(self, parent=None, letter=''):
    self.letter = StringVar()
    self.letter.set(letter)

    Label.__init__(self, parent, textvariable=self.letter)
    self.config(bd=1, height=2, font=('times', 14, 'bold'), width=4, relief=SUNKEN)

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
