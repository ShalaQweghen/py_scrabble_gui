from tkinter import *

# from side_frame import SideFrame
from tile import BoardTile, RackTile

from lib.dic import Dict
from lib.bag import Bag
from lib.word import Word
from lib.board import Board

class GamePage(Frame):
  def __init__(self, parent, controller, **options):
    self.dict = Dict('./dics/sowpods.txt')
    self.bag = Bag()
    self.board = Board()
    self.start = None
    self.controller = controller
    self.letters = {}
    self.move = None
    self.word = None
    self.empty_tiles = []

    Frame.__init__(self, parent, **options)

    self.draw()

  def draw_board(self):
    out_f = Frame(self, padx=30, bg='azure')
    out_f.pack()

    infobar = Frame(out_f, pady=20, bg='azure')
    infobar.pack(side=TOP, fill=X)

    my_sc = Label(infobar, text='My Score = 15')
    my_sc.config(height=2, bg='#ADFF2F', fg='#1a1a1a', padx=5)
    my_sc.pack(side=LEFT, padx=13)

    op_sc = Label(infobar, text='Opponent\'s Score = 115')
    op_sc.config(height=2, fg='#1a1a1a', bg='#FF4500', padx=5)
    op_sc.pack(side=LEFT, padx=13)

    bag = Label(infobar, text='Tiles in Bag = 75')
    bag.config(height=2, bg='dark gray', fg='white', padx=5)
    bag.pack(side=LEFT, padx=13)

    time = Label(infobar, text='Time Left = 15 min')
    time.config(height=2, bg='dark gray', fg='white', padx=5)
    time.pack(side=LEFT, padx=13)

    # SideFrame(TOP, range(1, 16), out_f)
    # SideFrame(BOTTOM, range(1, 16), out_f)
    # SideFrame(LEFT, range(97, 112), out_f)
    # SideFrame(RIGHT, range(97, 112), out_f)

    board_f = Frame(out_f)
    board_f.pack()

    row = 0
    row_n = 15
    while row < 15:
      col = 0
      col_n = 'a'
      while col < 15:
        t = BoardTile(row, col, board_f)
        t.name = col_n + str(row_n)
        t.bind('<1>', self.place_tile)
        col += 1
        col_n = chr(ord(col_n) + 1)
      row += 1
      row_n -= 1

  def draw_rack(self):
    rack = Frame(self, pady=15, bg='azure')
    rack.pack()

    for i in range(7):
      t = RackTile(rack, self.bag.draw())
      t.bind('<1>', self.place_tile)

  def draw_buttons(self):
    button_f = Frame(self, bg='azure')
    button_f.pack()

    Button(button_f, text='Submit', command=self.construct_move).pack(side=LEFT, padx=5)
    Button(button_f, text='Pass').pack(side=LEFT, padx=5)
    Button(button_f, text='Challenge').pack(side=LEFT, padx=5)

  def draw(self):
    self.draw_board()
    self.draw_rack()
    self.draw_buttons()

  def place_tile(self, event):
    start_name = type(self.start).__name__
    widget_name = type(event.widget).__name__
    widget_var = event.widget.var

    if start_name == 'RackTile' and self.start.var.get() != '':
      if widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.var.get())
          self.letters[event.widget.name] = event.widget
          self.empty_tiles.append(self.start)
          self.start.var.set('')
          self.start = None
      elif widget_name == 'RackTile':
        temp = widget_var.get()
        widget_var.set(self.start.var.get())
        self.start.var.set(temp)
        self.start = None
      else:
        self.start = None
    elif start_name == 'BoardTile' and self.start.var.get() != '' and self.start.active:
      if widget_name == 'RackTile' and widget_var.get() == '':
        widget_var.set(self.start.var.get())
        del self.letters[self.start.name]
        del self.empty_tiles[self.empty_tiles.index(event.widget)]
        self.start.var.set('')
        self.start = None
      elif widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.var.get())
          del self.letters[self.start.name]
          self.letters[event.widget.name] = event.widget
          self.start.var.set('')
          self.start = None
        elif widget_var.get() == self.start.var.get():
          self.start = None
        else:
          temp = widget_var.get()
          widget_var.set(self.start.var.get())
          self.start.var.set(temp)
          self.letters[self.start.name] = self.start
          self.letters[event.widget.name] = event.widget
          self.start = None
    else:
      self.start = event.widget

  def construct_move(self):
    word = []
    sorted_keys = sorted(self.letters)
    check1 = sorted_keys[0][0]
    check2 = sorted_keys[-1][0]

    if check1 == check2:
      direction = 'd'
      sorted_keys.reverse()
    else:
      direction = 'r'

    for key in sorted_keys:
      word.append(self.letters[key].var.get())

    self.word = Word(sorted_keys[0], direction, ''.join(word), self.board, self.dict)

    if self.word.validate():
      for key in sorted_keys:
        self.letters[key].active = False
        self.board.board[key] = self.letters[key].var.get()

      move = [sorted_keys[0], direction, ''.join(word)]
      self.move = ' '.join(move)
      self.letters = {}
      self.draw_letters()

  def draw_letters(self):
    for tile in self.empty_tiles:
      tile.var.set(self.bag.draw())

    self.empty_tiles = []



