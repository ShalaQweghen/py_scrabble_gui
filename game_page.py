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
    self.chal_mode = self.options.get('challenge_mode', False)
    self.comp_mode = self.options.get('comp_mode', False)
    self.norm_mode = self.options.get('normal_mode', False)
    self.lan_mode = self.options.get('lan_mode', False)
    self.time_limit = self.options.get('time_limit', 0)
    self.players= self.options['names']
    self.play_num = self.options['players']

    self.word = None
    self.start = None
    self.wild_tile = None
    self.over = False
    self.not_proceed = False
    self.op_score = 0
    self.cur_play_mark = 0
    self.letters = {}
    self.gui_board = {}
    self.used_spots = {}
    self.rack = []
    self.raw_word = []
    self.prev_words = []
    self.empty_tiles = []
    self.new_letters = []
    self.player_racks = []
    self.player_scores = []
    self.letter_buffer = []
    self.old_letter_buffer = []

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.bag_var = StringVar()
    self.time_var = StringVar()
    self.status_var = StringVar()
    self.words_var = StringVar()

    if self.time_limit:
      self.seconds = 0
      self.minutes = self.time_limit

    self.draw()
    self.initialize_game()

  def draw_board(self):
    out_f = Frame(self, padx=30, bg='azure')
    out_f.pack(side=LEFT)

    Label(out_f, textvariable=self.status_var, bg='azure', fg='#FF4500', font=('times', 25, 'italic')).pack(side=TOP, pady=15)

    # SideFrame(TOP, range(1, 16), out_f)
    # SideFrame(BOTTOM, range(1, 16), out_f)
    # SideFrame(LEFT, range(97, 112), out_f)
    # SideFrame(RIGHT, range(97, 112), out_f)

    board_f = Frame(out_f)
    board_f.pack(side=TOP)

    row = 0
    row_n = 15

    while row < 15:
      col = 0
      col_n = 'a'

      while col < 15:
        t = BoardTile(row, col, board_f)
        t.bind('<1>', self.place_tile)
        t.name = col_n + str(row_n)
        self.determine_background(t)

        self.gui_board[t.name] = t

        col += 1
        col_n = chr(ord(col_n) + 1)

      row += 1
      row_n -= 1

    rack = Frame(out_f, pady=15, bg='azure')
    rack.pack(side=TOP)

    for i in range(7):
      t = RackTile(rack)
      t.bind('<1>', self.place_tile)
      t['bg'] = '#BE975B'

      if self.norm_mode:
        t['fg'] = '#BE975B'

      self.rack.append(t)

    button_f = Frame(out_f, bg='azure')
    button_f.pack(side=TOP)

    self.sub = Button(button_f, text='Submit', bg='azure', command=self.process_word)
    self.sub.pack(side=LEFT, padx=5)

    self.pas = Button(button_f, text='Pass', bg='azure', command=self.pass_popup)
    self.pas.pack(side=LEFT, padx=5)

    if self.chal_mode:
      self.chal = Button(button_f, bg='azure', text='Challenge', command=self.challenge)
      self.chal.pack(side=LEFT, padx=5)

    if self.norm_mode:
      Button(button_f, text='Reveal', command=self.reveal).pack()

  def draw_info_frame(self):
    info_frame = Frame(self, bg='azure')
    info_frame.pack(side=LEFT)

    options = {'font': ('times', 15, 'italic'), 'bg': 'azure', 'fg': '#004d00'}

    if self.time_limit:
      Label(info_frame, textvariable=self.time_var, font=('times', 15, 'italic'), bg='#004d00', fg='azure').pack(side=TOP, anchor=NW)

    Label(info_frame, textvariable=self.bag_var, **options).pack(side=TOP, anchor=NW, pady=10)

    lf = LabelFrame(info_frame, pady=5, padx=5, bg='azure')
    lf.pack(side=TOP, anchor=NW)

    self.pl1_var = StringVar()
    Label(lf, textvariable=self.pl1_var, **options).pack(side=TOP, anchor=NW)

    self.pl2_var = StringVar()
    Label(lf, textvariable=self.pl2_var, **options).pack(side=TOP, anchor=NW)

    if self.play_num >= 3:
      print(1)
      self.pl3_var = StringVar()
      Label(lf, textvariable=self.pl3_var, **options).pack(side=TOP, anchor=NW)

    if self.play_num == 4:
      print(2)
      self.pl4_var = StringVar()
      Label(lf, textvariable=self.pl4_var, **options).pack(side=TOP, anchor=NW)

    Label(info_frame, text='Words:', **options).pack(side=TOP, anchor=NW, pady=10)

    Label(info_frame, textvariable=self.words_var, **options).pack(side=TOP, anchor=NW)

  def determine_background(self, t):
    if t.name in 'a1 a8 a15 h15 o15 h1 o8 o1'.split():
      t['bg'] = '#ff3300'
    elif t.name in 'h8 b2 c3 d4 e5 b14 c13 d12 e11 n2 m3 l4 k5 n14 m13 l12 k11'.split():
      t['bg'] = '#ff99cc'
    elif t.name in 'b6 b10 n6 n10 f2 f6 f10 f14 j2 j6 j10 j14'.split():
      t['bg'] = '#3366ff'
    elif t.name in 'a4 a12 c7 c9 d1 d8 d15 g3 g7 g9 g13 h4 h12 o4 o12 m7 m9 l1 l8 l15 i3 i7 i9 i13'.split():
      t['bg'] = '#b3c6ff'
    else:
      t['bg'] = '#ffd6cc'

  def draw(self):
    self.draw_board()
    self.draw_info_frame()

  def pass_popup(self):
    w = Toplevel(self)

    f = Frame(w)
    f.pack(side=TOP)

    self.master.master.update()
    x = self.master.master.winfo_rootx() + 200
    w.geometry("+{}+{}".format(x, 300))

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

  def set_word_info(self):
    mes = ''

    for word in self.word.words:
      mes = mes + ('{} {}\n'.format(word, self.word.words[word]))

    if len(self.empty_tiles) == 7:
      mes = mes + ('\nBonus 60')

    self.words_var.set(mes[:-1])

  def normalize_board(self):
    self.sub.config(state=NORMAL)
    self.pas.config(state=NORMAL)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = True

    self.status_var.set('... Player\'s Turn ...')
    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))
    self.pl2_var.set('Computer: {}'.format(self.player_scores[1]))

  def reveal(self):
    for t in self.rack:
      t['fg'] = 'black'

  def place_tile(self, event):
    start_name = type(self.start).__name__
    widget_name = type(event.widget).__name__
    widget_var = event.widget.var

    if start_name == 'RackTile' and self.start.var.get() != '':
      if widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.var.get())
          event.widget['bg'] = self.start['bg']

          self.letters[event.widget.name] = event.widget
          self.letter_buffer.append(event.widget)
          self.empty_tiles.append(self.start)

          self.start['bg'] = '#cccccc'
          self.start.var.set('')
          self.start = None
      elif widget_name == 'RackTile':
        temp = widget_var.get()
        widget_var.set(self.start.var.get())

        if event.widget in self.empty_tiles:
          self.empty_tiles.append(self.start)
          del self.empty_tiles[self.empty_tiles.index(event.widget)]

          event.widget['bg'] = '#BE975B'
          self.start['bg'] = '#cccccc'

        self.start.var.set(temp)
        self.start = None
      else:
        self.start = None
    elif start_name == 'BoardTile' and self.start.var.get() != '' and self.start.active:
      if widget_name == 'RackTile' and widget_var.get() == '':
        del self.letters[self.start.name]
        del self.empty_tiles[self.empty_tiles.index(event.widget)]

        self.letter_buffer.remove(self.start)

        widget_var.set(self.start.var.get())
        event.widget['bg'] = '#BE975B'

        self.determine_background(self.start)

        self.start.var.set('')
        self.start = None
      elif widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.var.get())
          event.widget['bg'] = self.start['bg']

          self.update_buffer_letters(event.widget)
          self.determine_background(self.start)

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

          self.update_buffer_letters(event.widget)

          self.letters[self.start.name] = self.start
          self.letters[event.widget.name] = event.widget
          self.start = None
    else:
      self.start = event.widget

  def update_buffer_letters(self, tile):
    for it in self.letter_buffer:
      if it.name == self.start.name:
        self.letter_buffer.remove(it)
        self.letter_buffer.append(tile)

  def initialize_game(self):
    if self.comp_mode:
      self.opponent = AIOpponent()

    if self.time_limit:
      print(1)
      self.countdown()

    self.initialize_players()

  def initialize_players(self):
    for i in range(self.play_num):
      self.player_scores.append(0)

      rack = []

      for j in range(7):
        rack.append(self.bag.draw())

      self.player_racks.append(rack)

    if self.comp_mode:
      self.opponent.letters = self.player_racks[1]

    self.switch_player()

  def decorate_rack(self):
    rack = self.player_racks[self.cur_play_mark]

    for l, t in zip(rack, self.rack):
      if l == '@':
        t.var.set(' ')
      else:
        t.var.set(l)

      if self.norm_mode:
        t['fg'] = '#BE975B'

  def update_racks(self):
    self.player_racks[self.cur_play_mark] = [x.var.get() for x in self.rack]

  def switch_player(self):
    if self.norm_mode:
      self.cur_play_mark = (self.cur_play_mark + 1) % self.play_num

    self.update_info()
    self.decorate_rack()

  def update_info(self):
    self.status_var.set('... {}\'s Turn ...'.format(self.players[self.cur_play_mark]))

    self.pl1_var.set('{}: {}'.format(self.players[0], self.player_scores[0]))
    self.pl2_var.set('{}: {}'.format(self.players[1], self.player_scores[1]))

    if self.play_num >= 3:
      self.pl3_var.set('{}: {}'.format(self.players[2], self.player_scores[2]))

    if self.play_num == 4:
      self.pl4_var.set('{}: {}'.format(self.players[3], self.player_scores[3]))

    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))

  def draw_letters(self):
    self.new_letters = []

    for tile in self.empty_tiles:
      tile.var.set(self.bag.draw())
      tile['bg'] = '#BE975B'

      self.new_letters.append(tile.var.get())

    self.empty_tiles = []

  def get_ai_move(self):
    word = self.opponent.get_move(self.bag, self.board, self.dict)

    for s, l in zip(word.range, word.word):
      if self.gui_board.get(s, False):
        self.gui_board[s].var.set(l)
        self.gui_board[s]['bg'] = '#BE975B'
        self.gui_board[s].active = False

        self.used_spots[s] = self.gui_board[s]

        del self.gui_board[s]

    self.player_scores[1] += word.points

    self.board.place(word.word, word.range)
    self.opponent.update_rack(self.bag)

    self.set_word_info()
    self.normalize_board()

  def wait_comp(self):
    self.sub.config(state=DISABLED)
    self.pas.config(state=DISABLED)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = False

    self.pl1_var.set('Player: {}'.format(self.player_scores[self.cur_play_mark]))
    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))
    self.status_var.set('... Computer\'s Turn ...')

    self.thread = threading.Thread(target=self.get_ai_move, args=())
    self.thread.start()

  def process_word(self):
    if self.letters:
      self.sorted_keys = sorted(self.letters)

      self.raw_word = []
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
        self.raw_word.append(self.letters[key].var.get())
        self.add_letters_on_board(key)

      offset = 0
      length = len(self.sorted_keys)

      for spot, index, letter in self.aob_list:
        if index < 0:
          index = 0
        elif index > length:
          index = length - 1

        self.raw_word.insert(index + offset, letter)
        self.sorted_keys.insert(index + offset, spot)

        offset += 1

      self.raw_word = ''.join(self.raw_word)

      if ' ' in self.raw_word:
        self.wild_tile_popup()

      self.word = Word(self.sorted_keys[0], self.direction, self.raw_word, self.board, self.dict, self.chal_mode)

      if not self.valid_sorted_letters():
        self.not_proceed = True

      if not self.not_proceed and self.word.validate():
        self.wild_tile = None
        self.prev_words = []

        for key in self.sorted_keys:
          if key in self.letters:
            self.letters[key].active = False
            self.used_spots[key] = self.gui_board[key]

            del self.gui_board[key]

        self.letters = {}

        self.player_scores[self.cur_play_mark] += self.word.calculate_total_points()

        if len(self.empty_tiles) == 7:
          self.player_scores[self.cur_play_mark] += 60

        self.board.place(self.raw_word, self.sorted_keys)

        self.set_word_info()

        self.prev_words.append(self.word.word)
        self.prev_words.extend([x[0] for x in self.word.extra_words])

        self.draw_letters()
        self.update_racks()

        self.start = None
        self.old_letter_buffer = self.letter_buffer.copy()
        self.letter_buffer = []

        if self.norm_mode:
          self.switch_player()
        else:
          self.wait_comp()
      else:
        if self.wild_tile:
          self.wild_tile.var.set(' ')
          self.wild_tile = None

        self.not_proceed = False

  def countdown(self):
    if self.seconds == 0:
      self.seconds = 59
      self.minutes -= 1
    else:
      self.seconds -= 1

    if self.seconds >= 0 and self.minutes >= 0:
      if self.seconds > 9:
        seconds = str(self.seconds)
      else:
        seconds = '0' + str(self.seconds)

      self.time_var.set('{}:{} Left'.format(self.minutes, seconds))
      self.master.master.after(1000, self.countdown)
    else:
      self.over = True

  def wild_tile_popup(self):
    w = Toplevel(self)

    f = Frame(w)
    f.pack(side=TOP)

    self.master.master.update()
    x = self.master.master.winfo_rootx() + 200
    w.geometry("+{}+{}".format(x, 300))

    Label(f, text='Enter a Letter:').pack(side=LEFT)

    e = Entry(f, width=2)
    e.pack(side=LEFT)
    e.focus()

    bf = Frame(w)
    bf.pack(side=BOTTOM)

    Button(bf, text='Submit', command=lambda: self.change_wild_tile(e)).pack(side=LEFT)
    Button(bf, text='Cancel', command=lambda: self.cancel_wild_tile_popup(w)).pack()

    w.grab_set()
    w.focus_set()
    w.wait_window()

  def valid_sorted_letters(self):
    if self.direction == 'd':
      check1 = int(self.sorted_keys[0][1:])
      check2 = self.sorted_keys[0][0]

      for key in self.sorted_keys[1:]:
        if int(key[1:]) != check1 - 1:
          return False

        if key[0] != check2:
          return False

        check1 -= 1
    else:
      check1 = ord(self.sorted_keys[0][0])
      check2 = self.sorted_keys[0][1:]

      for key in self.sorted_keys[1:]:
        if ord(key[0]) != check1 + 1:
          return False

        if key[1:] != check2:
          return False

        check1 += 1

    return True

  def cancel_move(self):
    for t1, t2 in zip(self.empty_tiles, self.letters.values()):
      t1.var.set(t2.var.get())
      t2.var.set('')
      t1['bg'] = '#BE975B'
      self.determine_background(t2)

    self.letters = {}
    self.not_proceed = True

  def cancel_wild_tile_popup(self, popup):
    popup.destroy()
    self.cancel_move()

  def change_wild_tile(self, ent):
    self.raw_word = re.sub(' ', ent.get().upper(), self.raw_word)

    for tile in self.letters:
      if self.letters[tile].var.get() == ' ':
        self.wild_tile = self.letters[tile]

        if self.chal_mode:
          self.wild_tile_clone = self.wild_tile

        self.board.wild_tiles_on_board.append(self.wild_tile.name)

        self.letters[tile].var.set(ent.get().upper())

    ent.master.master.destroy()

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

  def pass_letters(self, entry):
    passed_letters = list(re.sub('[^A-Z@]', '', entry.get().upper()))

    for tile in self.rack:
      if tile.var.get() in passed_letters:
        self.bag.put_back([tile.var.get()])
        del passed_letters[passed_letters.index(tile.var.get())]
        tile.var.set(self.bag.draw())

    entry.master.master.destroy()

    if self.norm_mode:
      self.switch_player()
    else:
      self.wait_comp()

  def challenge(self):
    if self.chal_mode:
      for word in self.prev_words:
        if not self.dict.valid_word(word):
          self.player_scores[self.cur_play_mark - 1] -= self.word.points

          if len(self.new_letters) == 7:
            self.player_scores[self.cur_play_mark - 1] -= 60

          for new in self.new_letters:
            self.player_racks[self.cur_play_mark - 1].remove(new)
            self.bag.put_back([new])

          for tile in self.old_letter_buffer:
            if tile.name in self.used_spots:
              if tile is self.wild_tile_clone:
                self.board.wild_tiles_on_board.remove(tile.name)
                tile.var.set(' ')

              self.player_racks[self.cur_play_mark -1].append(tile.var.get())
              self.board.board[tile.name] = ' '

              tile.var.set('')
              tile.active = True
              self.determine_background(tile)

              del self.used_spots[tile.name]

              self.gui_board[tile.name] = tile

          self.prev_words = []
          self.old_letter_buffer = []

          self.update_info()

          return

      self.switch_player()