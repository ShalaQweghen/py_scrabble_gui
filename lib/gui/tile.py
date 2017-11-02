# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import sys

from tkinter import *

# Height and width options are treated differently on Mac
if sys.platform == 'darwin':
  height = 2
  width = 4
elif sys.platform == 'win32':
  height = 1
  width = 2
else:
  height = 1
  width = 3

class Tile(Label):
  def __init__(self, parent=None, letter=''):
    self.letter = StringVar()
    self.letter.set(letter)

    Label.__init__(self, parent, textvariable=self.letter)
    self.config(bd=1,
                height=height,
                font=('times', 14, 'bold'),
                width=width,
                relief=SUNKEN)

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
