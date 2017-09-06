import threading

from tkinter import *

from side_frame import SideFrame
from tile import BoardTile, RackTile

from lib.dic import Dict
from lib.bag import Bag
from lib.word import Word
from lib.board import Board
from lib.comp import AIOpponent

class GamePage(Frame):
  def __init__(self, parent, controller):
    self.controller = controller

    self.dict = Dict('./dics/sowpods.txt')
    self.bag = Bag()
    self.board = Board()
    self.opponent = AIOpponent()

    self.opponent.draw_letters(self.bag)

    self.op_score = 0
    self.my_score = 0
    self.start = None
    self.letters = {}
    self.word = None
    self.empty_tiles = []
    self.gui_board = {}
    self.used_spots = {}

    Frame.__init__(self, parent, bg='azure')

    self.status_var = StringVar()
    self.my_var = StringVar()
    self.op_var = StringVar()
    self.bag_var = StringVar()
    self.time_var = StringVar()

    self.my_var.set('My Score = 0')
    self.op_var.set('Opponent\'s Score = 0')
    self.bag_var.set('Tiles in Bag = 86')
    self.time_var.set('Time Left = {} mins'.format(u'\u221e'))

    self.draw()

  def draw_board(self):
    out_f = Frame(self, padx=30, bg='azure')
    out_f.pack()

    infobar = Frame(out_f, pady=20, bg='azure')
    infobar.pack(side=TOP, fill=X)

    my_sc = Label(infobar, textvariable=self.my_var)
    my_sc.config(height=2, bg='#ADFF2F', fg='#1a1a1a', padx=5)
    my_sc.pack(side=LEFT, padx=13)

    op_sc = Label(infobar, textvariable=self.op_var)
    op_sc.config(height=2, fg='#1a1a1a', bg='#FF4500', padx=5)
    op_sc.pack(side=LEFT, padx=13)

    bag = Label(infobar, textvariable=self.bag_var)
    bag.config(height=2, bg='dark gray', fg='white', padx=5)
    bag.pack(side=LEFT, padx=13)

    time = Label(infobar, textvariable=self.time_var)
    time.config(height=2, bg='dark gray', fg='white', padx=5)
    time.pack(side=LEFT, padx=13)

    SideFrame(TOP, range(1, 16), out_f)
    SideFrame(BOTTOM, range(1, 16), out_f)
    SideFrame(LEFT, range(97, 112), out_f)
    SideFrame(RIGHT, range(97, 112), out_f)

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
        self.gui_board[t.name] = t
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

    self.sub = Button(button_f, text='Submit', command=self.construct_move)
    self.sub.pack(side=LEFT, padx=5)
    self.pas = Button(button_f, text='Pass')
    self.pas.pack(side=LEFT, padx=5)
    self.chal = Button(button_f, text='Challenge')
    self.chal.pack(side=LEFT, padx=5)

  def draw(self):
    self.draw_board()
    self.draw_rack()
    self.draw_buttons()
    Label(self, textvariable=self.status_var, bg='azure', fg='#FF4500').pack()

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

        if event.widget in self.empty_tiles:
          del self.empty_tiles[self.empty_tiles.index(event.widget)]
          self.empty_tiles.append(self.start)

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

  def get_ai_move(self):
    self.opponent.word = None
    word = self.opponent.get_move(self.bag, self.board, self.dict)

    for s, l in zip(word.range, word.word):
      if self.gui_board.get(s, False):
        self.gui_board[s].active = False
        self.gui_board[s].var.set(l)
        self.used_spots[s] = self.gui_board[s]
        del self.gui_board[s]

    self.board.place(word.word, word.range)

    self.opponent.update_rack(self.bag)

    self.sub.config(state=NORMAL)
    self.pas.config(state=NORMAL)
    self.chal.config(state=NORMAL)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = True

    self.status_var.set('')
    self.op_score += word.points
    self.bag_var.set('Tiles in Bag = {}'.format(len(self.bag.bag)))
    self.op_var.set('Opponent\'s Score = {}'.format(self.op_score))


  def construct_move(self):
    self.sorted_keys = sorted(self.letters)

    raw_word = []
    check1 = self.sorted_keys[0][0]
    check2 = self.sorted_keys[-1][0]

    if check1 == check2:
      self.direction = 'd'
      n = sorted([int(x[1:]) for x in self.sorted_keys])
      self.sorted_keys = [check1 + str(x) for x in n]
      self.sorted_keys.reverse()
    else:
      self.direction = 'r'

    for key in self.sorted_keys:
      raw_word.append(self.letters[key].var.get())

    self.aob_list = []

    for key in self.sorted_keys:
      self.add_letters_on_board(key)

    offset = 0
    leng = len(self.sorted_keys)
    for s, i, l in self.aob_list:
      if i < 0:
        i = 0
      elif i > leng:
        i = leng - 1

      self.sorted_keys.insert(i + offset, s)
      raw_word.insert(i + offset, l)
      offset += 1

    self.word = Word(self.sorted_keys[0], self.direction, ''.join(raw_word), self.board, self.dict)

    if self.word.validate():
      for key in self.sorted_keys:
        if key in self.letters:
          self.letters[key].active = False
          self.used_spots[key] = self.gui_board[key]
          del self.gui_board[key]

      self.board.place(raw_word, self.sorted_keys)

      self.letters = {}
      self.my_score += self.word.calculate_total_points()
      self.draw_letters()

      self.sub.config(state=DISABLED)
      self.pas.config(state=DISABLED)
      self.chal.config(state=DISABLED)

      for k, v in self.gui_board.items():
        self.gui_board[k].active = False

      self.my_var.set('My Score = {}'.format(self.my_score))
      self.bag_var.set('Tiles in Bag = {}'.format(len(self.bag.bag)))

      self.status_var.set('... Opponent\'s Turn ...')

      self.thread = threading.Thread(target=self.get_ai_move, args=())
      self.thread.start()
      print(threading.active_count())

  def draw_letters(self):
    for tile in self.empty_tiles:
      tile.var.set(self.bag.draw())

    self.empty_tiles = []

  def add_letters_on_board(self, spot):
    if self.direction == 'd':
      flag = True
      bef = spot[0] + str(int(spot[1:]) + 1)
      aft = spot[0] + str(int(spot[1:]) - 1)
      check = [x[0] for x in self.aob_list if x[0] == aft or x[0] == bef]
      while flag and not check:
        if aft not in self.gui_board and int(aft[1:]) in range(1, 16):
          self.aob_list.append((aft, self.sorted_keys.index(spot) + 1, self.used_spots[aft].var.get()))
          aft = aft[0] + str(int(aft[1:]) - 1)
        elif bef not in self.gui_board and int(bef[1:]) in range(1, 16):
          self.aob_list.insert(0, (bef, self.sorted_keys.index(spot) - 1, self.used_spots[bef].var.get()))
          bef = bef[0] + str(int(bef[1:]) + 1)
        else:
          flag = False
    else:
      flag = True
      bef = chr(ord(spot[0]) - 1) + spot[1:]
      aft = chr(ord(spot[0]) + 1) + spot[1:]
      check = [x[0] for x in self.aob_list if x[0] == aft or x[0] == bef]
      while flag and not check:
        if aft not in self.gui_board and ord(aft[0]) in range(97, 112):
          self.aob_list.append((aft, self.sorted_keys.index(spot) + 1, self.used_spots[aft].var.get()))
          aft = chr(ord(aft[0]) + 1) + aft[1:]
        elif bef not in self.gui_board and ord(bef[0]) in range(97, 112):
          self.aob_list.insert(0, (bef, self.sorted_keys.index(spot) - 1, self.used_spots[bef].var.get()))
          bef = chr(ord(bef[0]) - 1) + bef[1:]
        else:
          flag = False