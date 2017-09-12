import threading, re, os, pickle

from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename

from lib.gui.tile import BoardTile, RackTile

from lib.dic import Dict
from lib.bag import Bag
from lib.word import Word
from lib.board import Board
from lib.comp import AIOpponent
from lib.player import Player

class GamePage(Frame):
  def __init__(self, parent, options, dic='./dics/sowpods.txt'):
    self.dict = Dict(dic)
    self.bag = Bag()
    self.board = Board()

    self.options = options
    self.chal_mode = self.options.get('challenge_mode', False)
    self.comp_mode = self.options.get('comp_mode', False)
    self.norm_mode = self.options.get('normal_mode', False)
    self.lan_mode = self.options.get('lan_mode', False)
    self.time_limit = self.options.get('time_limit', 0)
    self.point_limit = self.options.get('point_limit', 0)
    self.players = self.options.get('names', [])
    self.play_num = self.options.get('players', 0)
    self.loading = self.options.get('loading', False)

    self.minutes = self.time_limit

    self.word = None
    self.start = None
    self.winner = None
    self.wild_tile = None
    self.cur_player = None
    self.wild_tile_clone = None
    self.over = False
    self.time_up = False
    self.may_proceed = True
    self.changing_wild_tile = False
    self.seconds = 0
    self.op_score = 0
    self.pass_num = 0
    self.cur_play_mark = 0
    self.letters = {}
    self.gui_board = {}
    self.used_spots = {}
    self.rack = []
    self.losers = []
    self.raw_word = []
    self.prev_words = []
    self.empty_tiles = []
    self.letter_buffer = []
    self.old_letter_buffer = []

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.bag_var = StringVar()
    self.time_var = StringVar()
    self.status_var = StringVar()
    self.words_var = StringVar()

    self.draw_main_frame()
    self.draw_info_frame()
    self.initialize_game()

  def draw_main_frame(self):
    out_f = Frame(self, padx=30, bg='azure')
    out_f.pack(side=LEFT)

    Label(out_f, textvariable=self.status_var, bg='azure', fg='#FF4500', font=('times', 25, 'italic')).pack(side=TOP, pady=15)

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

    self.pas = Button(button_f, text='Pass', bg='azure', command=lambda: self.show_popup('Pass Letters', 'Enter letters to pass:', 'Pass', self.pass_letters))
    self.pas.pack(side=LEFT, padx=5)

    if self.chal_mode:
      self.chal = Button(button_f, bg='azure', text='Challenge', command=self.challenge)
      self.chal.pack(side=LEFT, padx=5)

    if self.norm_mode:
      Button(button_f, text='Reveal', command=self.reveal).pack()

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

  def reveal(self):
    for t in self.rack:
      t['fg'] = 'black'

  def draw_info_frame(self):
    info_frame = Frame(self, bg='azure')
    info_frame.pack(side=LEFT, fill=BOTH)

    self.sav = Button(info_frame, text='Save Game', command=self.save_game, bg='azure')
    self.sav.pack(side=TOP, pady=90)

    f = Frame(info_frame, bg='azure')
    f.pack(side=TOP, pady=50, fill=X)

    options = {'font': ('times', 15, 'italic'), 'bg': 'azure', 'fg': '#004d00'}

    if self.time_limit:
      Label(f, textvariable=self.time_var, font=('times', 15, 'italic'), bg='#004d00', fg='azure').pack(anchor=NW)

    Label(f, textvariable=self.bag_var, **options).pack(pady=10)

    lf = LabelFrame(f, pady=5, padx=5, bg='azure')
    lf.pack(anchor=NW)

    self.pl1_var = StringVar()
    Label(lf, textvariable=self.pl1_var, **options).pack(anchor=NW)

    self.pl2_var = StringVar()
    Label(lf, textvariable=self.pl2_var, **options).pack(anchor=NW)

    if self.play_num >= 3:
      self.pl3_var = StringVar()
      Label(lf, textvariable=self.pl3_var, **options).pack(anchor=NW)

    if self.play_num == 4:
      self.pl4_var = StringVar()
      Label(lf, textvariable=self.pl4_var, **options).pack(anchor=NW)

    Label(f, text='Words:', **options).pack(anchor=NW, pady=10)

    Message(f, textvariable=self.words_var, font=('times', 14, 'italic'), anchor=NW, bg='azure', fg='#004d00').pack(anchor=NW, fill=X)

  def set_word_info(self, word):
    mes = ''

    for w in word.words:
      mes = mes + ('{} {}\n'.format(w, word.words[w]))

    if self.cur_player.full_bonus:
      mes = mes + ('\nBonus 60\n')

    self.words_var.set(mes[:-1])

  def show_popup(self, title_text, label_text, button_text, command):
    if button_text == 'Set':
      self.changing_wild_tile = True

    w = Toplevel(self)
    w.title(title_text)

    w.protocol('WM_DELETE_WINDOW', lambda: self.cancel_popup(w))

    f = Frame(w)
    f.pack(side=TOP)

    self.master.master.update()
    x = self.master.master.winfo_rootx() + 200
    w.geometry("+{}+{}".format(x, 300))

    Label(f, text=label_text).pack(side=LEFT)

    e = Entry(f)
    e.pack(side=LEFT)
    e.focus()

    bf = Frame(w)
    bf.pack(side=BOTTOM)

    Button(bf, text=button_text, command=lambda: command(e)).pack(side=LEFT)
    Button(bf, text='Cancel', command=lambda: self.cancel_popup(w)).pack()

    w.grab_set()
    w.focus_set()
    w.wait_window()

  def cancel_move(self):
    for t1, t2 in zip(self.empty_tiles, self.letters.values()):
      t1.letter.set(t2.letter.get())
      t2.letter.set('')
      t1['bg'] = '#BE975B'
      self.determine_background(t2)

    self.letters = {}
    self.may_proceed = False

  def cancel_popup(self, popup):
    popup.destroy()

    if self.changing_wild_tile:
      self.cancel_move()
      self.changing_wild_tile = False

  def initialize_game(self):
    if self.time_limit:
      self.countdown()

    self.check_game_over()

    self.initialize_players()

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
      self.time_up = True

      self.end_game()

  def initialize_players(self):
    if not self.loading:
      for i in range(self.play_num):
        pl = Player(self.players[i])
        pl.draw_letters(self.bag)
        self.players.append(pl)

        if self.comp_mode:
          self.opponent = AIOpponent()
          self.opponent.draw_letters(self.bag)
          self.players.append(self.opponent)

          break

      del self.players[:self.play_num]

    if self.loading:
      self.master.master.after(1000, self.load_game)
    else:
      self.switch_player()

  def load_game(self):
    keys = []
    values = []

    for key, value in self.board.board.items():
      if re.fullmatch('[A-Z@]', value):
        keys.append(key)
        values.append(value)

    for key, value in self.gui_board.items():
      if key in keys:
        self.gui_board[key].letter.set(values[keys.index(key)])
        self.gui_board[key].active = False
        self.gui_board[key]['bg'] = '#BE975B'

        self.used_spots[key] = self.gui_board[key]

    for key in keys:
      del self.gui_board[key]

    self.switch_player()

  def switch_player(self):
    if self.norm_mode and not self.loading:
      self.cur_play_mark = (self.cur_play_mark + 1) % self.play_num

    self.cur_player = self.players[self.cur_play_mark]

    self.loading = False

    self.update_info()
    self.decorate_rack()

  def update_info(self):
    self.status_var.set('... {}\'s Turn ...'.format(self.cur_player.name))

    self.pl1_var.set('{}: {}'.format(self.players[0].name, self.players[0].score))
    self.pl2_var.set('{}: {}'.format(self.players[1].name, self.players[1].score))

    if self.play_num >= 3:
      self.pl3_var.set('{}: {}'.format(self.players[2].name, self.players[2].score))

    if self.play_num == 4:
      self.pl4_var.set('{}: {}'.format(self.players[3].name, self.players[3].score))

    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))

  def decorate_rack(self):
    for l, t in zip(self.cur_player.letters, self.rack):
      if l == '@':
        t.letter.set(' ')
      else:
        t.letter.set(l)

      t['bg'] = '#BE975B'

      if self.norm_mode:
        t['fg'] = '#BE975B'

    if len(self.bag.bag) == 0:
      for t in self.rack[len(self.cur_player.letters):]:
        t.letter.set('')
        t['bg'] = '#cccccc'

  def wait_comp(self):
    self.sub.config(state=DISABLED)
    self.pas.config(state=DISABLED)
    self.sav.config(state=DISABLED)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = False

    self.pl1_var.set('Player: {}'.format(self.cur_player.score))
    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))
    self.status_var.set('... Computer\'s Turn ...')

    self.thread = threading.Thread(target=self.get_ai_move, args=())
    self.thread.start()

  def get_ai_move(self):
    word = self.opponent.get_move(self.bag, self.board, self.dict)

    if self.opponent.is_passing:
      self.passes += 1
    else:
      self.passes = 0

      for s, l in zip(word.range, word.word):
        if self.gui_board.get(s, False):
          self.gui_board[s].letter.set(l)
          self.gui_board[s]['bg'] = '#BE975B'
          self.gui_board[s].active = False

          self.used_spots[s] = self.gui_board[s]

          del self.gui_board[s]

      self.set_word_info(word)

      self.opponent.update_rack(self.bag)
      self.opponent.update_score()
      self.decorate_rack()

      self.board.place(word.word, word.range)

    self.normalize_board()

  def update_rack(self):
    for rt, l in zip(self.rack, self.cur_player.letters):
      rt.letter.set(l)
      rt['bg'] = '#BE975B'

    if len(self.bag.bag) == 0:
      for i, rt in enumerate(self.rack):
        rt['bg'] = '#BE975B'
        if i == len(self.cur_player.letters) - 1:
          break

  def normalize_board(self):
    self.sub.config(state=NORMAL)
    self.pas.config(state=NORMAL)
    self.sav.config(state=NORMAL)

    for k, v in self.gui_board.items():
      self.gui_board[k].active = True

    self.status_var.set('... Player\'s Turn ...')
    self.bag_var.set('{} Tiles in Bag'.format(len(self.bag.bag)))
    self.pl2_var.set('Computer: {}'.format(self.players[1].score))

  def place_tile(self, event):
    start_name = type(self.start).__name__
    widget_name = type(event.widget).__name__
    widget_var = event.widget.letter

    if start_name == 'RackTile' and self.start.letter.get() != '':
      if widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.letter.get())
          event.widget['bg'] = self.start['bg']

          self.letters[event.widget.name] = event.widget
          self.letter_buffer.append(event.widget)
          self.empty_tiles.append(self.start)

          self.start['bg'] = '#cccccc'
          self.start.letter.set('')
          self.start = None
      elif widget_name == 'RackTile':
        temp = widget_var.get()
        widget_var.set(self.start.letter.get())

        if event.widget in self.empty_tiles:
          self.empty_tiles.append(self.start)
          del self.empty_tiles[self.empty_tiles.index(event.widget)]

          event.widget['bg'] = '#BE975B'
          self.start['bg'] = '#cccccc'

        self.start.letter.set(temp)
        self.start = None
      else:
        self.start = None
    elif start_name == 'BoardTile' and self.start.letter.get() != '' and self.start.active:
      if widget_name == 'RackTile' and widget_var.get() == '':
        del self.letters[self.start.name]
        del self.empty_tiles[self.empty_tiles.index(event.widget)]

        self.letter_buffer.remove(self.start)

        widget_var.set(self.start.letter.get())
        event.widget['bg'] = '#BE975B'

        self.determine_background(self.start)

        self.start.letter.set('')
        self.start = None
      elif widget_name == 'BoardTile' and event.widget.active:
        if widget_var.get() == '':
          widget_var.set(self.start.letter.get())
          event.widget['bg'] = self.start['bg']

          self.update_buffer_letters(event.widget)
          self.determine_background(self.start)

          del self.letters[self.start.name]

          self.letters[event.widget.name] = event.widget

          self.start.letter.set('')
          self.start = None
        elif widget_var.get() == self.start.letter.get():
          self.start = None
        else:
          temp = widget_var.get()
          widget_var.set(self.start.letter.get())
          self.start.letter.set(temp)

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
        self.raw_word.append(self.letters[key].letter.get())
        self.set_aob_list(key)

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
        self.show_popup('Set Wild Tile', 'Enter a letter:', 'Set', self.change_wild_tile)

      self.word = Word(self.sorted_keys[0], self.direction, self.raw_word, self.board, self.dict, self.chal_mode)

      self.word.set_aob_list([x[2] for x in self.aob_list])

      if not self.valid_sorted_letters():
        self.may_proceed = False

      if self.may_proceed and self.word.validate():
        self.cur_player.word = self.word

        self.pass_num = 0
        self.wild_tile = None
        self.prev_words = []

        for key in self.sorted_keys:
          if key in self.letters:
            self.letters[key].active = False
            self.used_spots[key] = self.gui_board[key]

            del self.gui_board[key]

        self.letters = {}

        self.cur_player.update_rack(self.bag)
        self.cur_player.update_score()
        self.decorate_rack()

        self.board.place(self.raw_word, self.sorted_keys)

        self.set_word_info(self.word)

        self.prev_words.append(self.word.word)
        self.prev_words.extend([x[0] for x in self.word.extra_words])

        self.empty_tiles = []

        self.start = None
        self.old_letter_buffer = self.letter_buffer.copy()
        self.letter_buffer = []

        if self.norm_mode:
          self.switch_player()
        else:
          self.wait_comp()
      else:
        if self.wild_tile:
          self.wild_tile.letter.set(' ')
          self.wild_tile = None

        self.may_proceed = True

  def set_aob_list(self, spot):
    flag = True

    if self.direction == 'd':
      bef = spot[0] + str(int(spot[1:]) + 1)
      aft = spot[0] + str(int(spot[1:]) - 1)
      check = [x[0] for x in self.aob_list if x[0] == aft or x[0] == bef]

      while flag and not check:
        if aft not in self.gui_board and int(aft[1:]) in range(1, 16):
          self.aob_list.append((aft, self.sorted_keys.index(spot) + 1, self.used_spots[aft].letter.get()))
          aft = aft[0] + str(int(aft[1:]) - 1)
        elif bef not in self.gui_board and int(bef[1:]) in range(1, 16):
          self.aob_list.insert(0, (bef, self.sorted_keys.index(spot) - 1, self.used_spots[bef].letter.get()))
          bef = bef[0] + str(int(bef[1:]) + 1)
        else:
          flag = False
    else:
      bef = chr(ord(spot[0]) - 1) + spot[1:]
      aft = chr(ord(spot[0]) + 1) + spot[1:]
      check = [x[0] for x in self.aob_list if x[0] == aft or x[0] == bef]

      while flag and not check:
        if aft not in self.gui_board and ord(aft[0]) in range(97, 112):
          self.aob_list.append((aft, self.sorted_keys.index(spot) + 1, self.used_spots[aft].letter.get()))
          aft = chr(ord(aft[0]) + 1) + aft[1:]
        elif bef not in self.gui_board and ord(bef[0]) in range(97, 112):
          self.aob_list.insert(0, (bef, self.sorted_keys.index(spot) - 1, self.used_spots[bef].letter.get()))
          bef = chr(ord(bef[0]) - 1) + bef[1:]
        else:
          flag = False

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

  def change_wild_tile(self, ent):
    if re.fullmatch('[A-Z@]', ent.get().upper()):
      self.raw_word = re.sub(' ', ent.get().upper(), self.raw_word)

      for tile in self.letters:
        if self.letters[tile].letter.get() == ' ':
          self.wild_tile = self.letters[tile]

          if self.chal_mode:
            self.wild_tile_clone = self.wild_tile

          self.board.wild_tiles_on_board.append(self.wild_tile.name)

          self.letters[tile].letter.set(ent.get().upper())

          self.cur_player.wild_tiles.append(ent.get().upper())

      ent.master.master.destroy()

  def pass_letters(self, entry):
    for key, value in self.gui_board.items():
      if value.letter.get() != '':
        self.empty_tiles[0].letter.set(value.letter.get())
        self.empty_tiles[0]['bg'] = '#BE975B'
        del self.empty_tiles[0]

        value.letter.set('')
        self.determine_background(value)

    passed_letters = list(re.sub('[^A-Z@]', '', entry.get().upper()))

    self.cur_player.set_passed_letters(passed_letters)

    entry.master.master.destroy()

    self.cur_player.update_rack(self.bag)
    self.decorate_rack()

    self.pass_num += 1

    if self.norm_mode:
      self.switch_player()
    else:
      self.wait_comp()

  def challenge(self):
    if self.chal_mode:
      for word in self.prev_words:
        if not self.dict.valid_word(word):
          self.players[self.cur_play_mark - 1].update_score(self.word.points)

          if len(self.players[self.cur_play_mark - 1].new_letters) == 7:
            self.players[self.cur_play_mark - 1].update_score(60)

          for new in self.players[self.cur_play_mark - 1].new_letters:
            self.players[self.cur_play_mark - 1].letters.remove(new)
            self.bag.put_back([new])

          for tile in self.old_letter_buffer:
            if tile.name in self.used_spots:
              if tile is self.wild_tile_clone:
                self.board.wild_tiles_on_board.remove(tile.name)
                tile.letter.set(' ')

              self.players[self.cur_play_mark -1].letters.append(tile.letter.get())
              self.board.board[tile.name] = ' '

              tile.letter.set('')
              tile.active = True
              self.determine_background(tile)

              del self.used_spots[tile.name]

              self.gui_board[tile.name] = tile

          self.prev_words = []
          self.old_letter_buffer = []

          self.update_info()

          return True

      self.switch_player()

      return False

  def check_game_over(self):
    if len(self.bag.bag) == 0:
      for pl in self.players:
        if len(pl.letters) == 0:
          self.end_game()

          return

      self.master.master.after(1000, self.check_game_over)
    elif self.pass_num == 3 * self.play_num:
      self.end_game()
    elif self.point_limit:
      for pl in self.players:
        if pl.score >= self.point_limit:
          self.end_game()

          return

      self.master.master.after(1000, self.check_game_over)
    else:
      self.master.master.after(1000, self.check_game_over)

  def end_game(self):
    if self.chal_mode and len(self.bag.bag) == 0 and [pl for pl in self.players if len(pl.letters) == 0]:
      challenged = askyesno('Challenge', 'Will you challenge any of \'{}\'?'.format(', '.join(self.prev_words))) and self.challenge()
    else:
      challenged = False

    if not challenged:
      self.determine_winner()

      if self.time_up:
        rea = 'Time Is Up'
      else:
        rea = 'Game Is Over'

      mes = '{} has won with {} points!'.format(self.winner[0], self.winner[1])

      self.show_end_game_popup(rea, mes)
    else:
      self.check_game_over()

  def show_end_game_popup(self, reason, message):
    w = Toplevel(self)
    w.title(reason)

    self.master.master.update()
    x = self.master.master.winfo_rootx() + 200
    w.geometry("+{}+{}".format(x, 300))

    w.protocol('WM_DELETE_WINDOW', lambda: self.quit_game(w))

    Label(w, text=message, font=('times', 30, 'italic')).pack(side=TOP, padx=50, pady=30)

    f = Frame(w)
    f.pack(side=TOP)

    if not self.point_limit and not self.time_limit:
      for pl, sub in self.losers:
        if sub > 0:
          Label(f, text='{} {} points for {} left on rack...'.format(pl.name, -sub, ', '.join(pl.letters))).pack(side=TOP)

    bf = Frame(w)
    bf.pack(side=TOP, pady=20)

    Button(bf, text='Quit', command=lambda: self.quit_game(w)).pack(side=LEFT, padx=15)
    Button(bf, text='Restart', command=self.restart_game).pack(side=LEFT)

    w.grab_set()
    w.focus_set()
    w.wait_window()

  def determine_winner(self):
    if not self.time_limit and not self.point_limit:
      for pl in self.players:
        sub = 0
        for l in pl.letters:
          sub += self.word.letter_points[l]
          pl.update_score(self.word.letter_points[l])

        self.losers.append((pl, sub))

    pts = max([pl.score for pl in self.players])
    ply = self.players[[pl.score for pl in self.players].index(pts)].name

    self.winner = (ply, pts)

  def quit_game(self, win):
    win.destroy()
    self.master.master.quit()

  def restart_game(self):
    self.master.master.geometry('704x420')
    self.master.master.minsize(704, 420)

    self.destroy()

  def save_game(self):
    if not os.path.exists('./saves'):
      os.mkdir('./saves')

    filename = asksaveasfilename(initialdir='saves', defaultextension='.pickle')

    if filename:
      data = {}
      data['play_num'] = self.play_num
      data['players'] = self.players
      data['pass_num'] = self.pass_num
      data['cur_play_mark'] = self.cur_play_mark
      data['chal_mode'] = self.chal_mode
      data['comp_mode'] = self.comp_mode
      data['norm_mode'] = self.norm_mode
      data['point_limit'] = self.point_limit
      data['time_limit'] = self.time_limit
      data['bag'] = self.bag
      data['board'] = self.board
      data['op_score'] = self.op_score
      data['seconds'] = self.seconds
      data['minutes'] = self.minutes

      file = open(filename, 'wb')
      pickle.dump(data, file)

