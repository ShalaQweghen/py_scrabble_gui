import threading, re

from tkinter import *

# from side_frame import SideFrame
from tile import BoardTile, RackTile

from lib.dic import Dict
from lib.bag import Bag
from lib.word import Word
from lib.board import Board
from lib.comp import AIOpponent

class GamePage(Frame):
  def __init__(self, parent, options):
    self.dict = Dict('./dics/sowpods.txt')
    self.bag = Bag()
    self.board = Board()

    self.options = options

    self.word = None
    self.start = None
    self.op_score = 0
    self.cur_play_mark = 0
    self.letters = {}
    self.gui_board = {}
    self.used_spots = {}
    self.rack = []
    self.empty_tiles = []
    self.player_racks = []
    self.player_scores = []

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.op_var = StringVar()
    self.bag_var = StringVar()
    self.time_var = StringVar()
    self.status_var = StringVar()
    self.player_var = StringVar()
    self.current_player = StringVar()

    self.time_var.set('Time Left = {} mins'.format(u'\u221e'))

    self.draw()
    self.initialize_game()

  def draw_board(self):
    out_f = Frame(self, padx=30, bg='azure')
    out_f.pack()

    infobar = Frame(out_f, pady=20, bg='azure')
    infobar.pack(side=TOP, fill=X)

    my_sc = Label(infobar, textvariable=self.player_var)
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
        t.bind('<1>', self.place_tile)
        t.name = col_n + str(row_n)

        self.gui_board[t.name] = t

        col += 1
        col_n = chr(ord(col_n) + 1)

      row += 1
      row_n -= 1

  def draw_rack(self):
    rack = Frame(self, pady=15, bg='azure')
    rack.pack()

    for i in range(7):
      t = RackTile(rack)
      t.bind('<1>', self.place_tile)

      self.rack.append(t)

  def draw_buttons(self):
    button_f = Frame(self, bg='azure')
    button_f.pack()

    self.sub = Button(button_f, text='Submit', command=self.process_word)
    self.sub.pack(side=LEFT, padx=5)

    self.pas = Button(button_f, text='Pass', command=self.pass_popup)
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
    word = self.opponent.get_move(self.bag, self.board, self.dict)

    for s, l in zip(word.range, word.word):
      if self.gui_board.get(s, False):
        self.gui_board[s].var.set(l)
        self.gui_board[s].active = False

        self.used_spots[s] = self.gui_board[s]

        del self.gui_board[s]

    self.op_score += word.points

    self.board.place(word.word, word.range)
    self.opponent.update_rack(self.bag)
    self.normalize_board()

  def normalize_board(self):
    self.sub.config(state=NORMAL)
    self.pas.config(state=NORMAL)
    self.chal.config(state=NORMAL)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = True

    self.status_var.set('')
    self.bag_var.set('Tiles in Bag = {}'.format(len(self.bag.bag)))
    self.op_var.set('Opponent\'s Score = {}'.format(self.op_score))


  def process_word(self):
    self.sorted_keys = sorted(self.letters)

    raw_word = []
    check1 = self.sorted_keys[0][0]
    check2 = self.sorted_keys[-1][0]

    if check1 == check2:
      digits = sorted([int(x[1:]) for x in self.sorted_keys])
      self.sorted_keys = [check1 + str(x) for x in digits]
      self.sorted_keys.reverse()

      self.direction = 'd'
    else:
      self.direction = 'r'

    self.aob_list = []

    for key in self.sorted_keys:
      raw_word.append(self.letters[key].var.get())
      self.add_letters_on_board(key)

    offset = 0
    length = len(self.sorted_keys)

    for spot, index, letter in self.aob_list:
      if index < 0:
        index = 0
      elif index > length:
        index = length - 1

      raw_word.insert(index + offset, letter)
      self.sorted_keys.insert(index + offset, spot)

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
      self.player_scores[self.cur_play_mark] += self.word.calculate_total_points()

      self.draw_letters()
      self.update_racks()

      if self.options.get('normal_mode'):
        self.switch_player()
      else:
        self.wait_comp()

  def initialize_game(self):
    self.initialize_players()

    if self.options.get('comp_mode', False):
      self.bag_var.set('Tiles in Bag = 86')
      self.op_var.set('Opponent\'s Score = 0')

      self.opponent = AIOpponent()
      self.opponent.draw_letters(self.bag)

  def initialize_players(self):
    self.current_player.set(self.options['names'][0].capitalize() + '\'s')

    for i in range(self.options['players']):
      self.player_scores.append(0)

      rack = []

      for i in range(7):
        rack.append(self.bag.draw())

      self.player_racks.append(rack)

    self.switch_player()

  def decorate_rack(self):
    rack = self.player_racks[self.cur_play_mark]

    for l, t in zip(rack, self.rack):
      t.var.set(l)

  def update_racks(self):
    self.player_racks[self.cur_play_mark] = [x.var.get() for x in self.rack]

  def switch_player(self):
    self.cur_play_mark = (self.cur_play_mark + 1) % self.options['players']

    self.current_player.set(self.options['names'][self.cur_play_mark].capitalize() + '\'s')
    self.player_var.set('{} Score = {}'.format(self.current_player.get(), self.player_scores[self.cur_play_mark]))
    self.bag_var.set('Tiles in Bag = {}'.format(len(self.bag.bag)))

    self.decorate_rack()

  def wait_comp(self):
    self.sub.config(state=DISABLED)
    self.pas.config(state=DISABLED)
    self.chal.config(state=DISABLED)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = False

    self.player_var.set('Player\'s Score = {}'.format(self.player_scores[self.cur_play_mark]))
    self.bag_var.set('Tiles in Bag = {}'.format(len(self.bag.bag)))
    self.status_var.set('... Opponent\'s Turn ...')

    self.thread = threading.Thread(target=self.get_ai_move, args=())
    self.thread.start()

  def draw_letters(self):
    for tile in self.empty_tiles:
      tile.var.set(self.bag.draw())

    self.empty_tiles = []

  def add_letters_on_board(self, spot):
    flag = True

    if self.direction == 'd':
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

  def pass_popup(self):
    w = Toplevel(self)

    f = Frame(w)
    f.pack(side=TOP)

    Label(f, text='Enter letters to pass:').pack(side=LEFT)

    e = Entry(f)
    e.pack(side=LEFT)
    e.focus()

    bf = Frame(w)
    bf.pack(side=BOTTOM)

    Button(bf, text='Pass', command=lambda: self.pass_letters(e)).pack(side=LEFT)
    Button(bf, text='Cancel', command=w.destroy).pack()

    w.grab_set()
    w.focus_set()
    w.wait_window()

  def pass_letters(self, entry):
    passed_letters = list(re.sub('[^A-Z@]', '', entry.get().upper()))

    for tile in self.rack:
      if tile.var.get() in passed_letters:
        self.bag.put_back([tile.var.get()])
        del passed_letters[passed_letters.index(tile.var.get())]
        tile.var.set(self.bag.draw())

    entry.master.master.destroy()

    if self.options.get('normal_mode', False):
      self.switch_player()
    else:
      self.wait_comp()