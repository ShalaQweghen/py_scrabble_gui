from tkinter import *

class Tile(Label):
  def __init__(self, parent=None, letter='', **options):
    self.var = StringVar()
    self.var.set(letter)

    Label.__init__(self, parent, textvariable=self.var, **options)
    self.config(bd=1, height=2, width=4, relief=SUNKEN)


class BoardTile(Tile):
  def __init__(self, row, col, parent=None, letter='', **options):
    Tile.__init__(self, parent, letter, **options)
    self.grid(row=row, column=col)

class RackTile(Tile):
  def __init__(self, parent=None, letter='', **options):
    Tile.__init__(self, parent, letter, **options)
    self.pack(side=LEFT)
