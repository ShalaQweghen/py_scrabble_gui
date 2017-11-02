# Copyright (C) 2017  Serafettin Yilmaz
#
# See 'py_scrabble.pyw' for more info on copyright

import random

from tkinter import *

from lib.gui.game_page import GamePage

class StartPage(Frame):
  def __init__(self, parent, dic='./dics/sowpods.txt'):
    self.parent = parent
    self.dict = dic

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.chal_var = IntVar()
    self.time_var = IntVar()
    self.point_var = IntVar()
    self.but_var = StringVar()

    self.but_var.set('Start Game')

    self.play_ents = []

    self.draw_heading()
    self.draw_player_name()

    self.opt_cont = Frame(self, bg='azure')
    self.opt_cont.pack(side=TOP, padx=96)

    self.draw_player_options()
    self.draw_secondary_options()

  def draw_heading(self):
    Label(self, text='OPTIONS', font=('times', 35, 'italic'), bg='azure', pady=40).pack(side=TOP)

  def draw_secondary_options(self):
    cb = Checkbutton(self, bg='azure', text='Challenge Mode', variable=self.chal_var)
    cb.pack(pady=15)
    cb.deselect()

    f1 = Frame(self, bg='azure')
    f1.pack()

    Label(f1, bg='azure', text='Time Limit:').pack(side=LEFT)

    Entry(f1, textvariable=self.time_var, width=3).pack(side=LEFT)
    self.time_var.set(0)

    f2 = Frame(self, bg='azure')
    f2.pack(pady=5)

    Label(f2, bg='azure', text='Point Limit:').pack(side=LEFT)

    Entry(f2, textvariable=self.point_var, width=3).pack(side=LEFT)
    self.point_var.set(0)

    Button(self, textvariable=self.but_var, command=self.construct_options).pack(pady=10)

  def draw_player_name(self): pass

  def draw_player_options(self): pass

  def construct_options(self): pass

############################################################################

class LANStartPage(StartPage):
  def draw_player_options(self):
    self.but_var.set('Start Game')

    f = Frame(self.opt_cont, pady=10, bg='azure')
    f.pack()

    self.name_var = StringVar()

    Label(f, text='Enter Your Name:', bg='azure').pack(side=LEFT)

    ent = Entry(f, textvariable=self.name_var)
    ent.pack(side=LEFT)
    ent.focus_set()

    self.play_var = IntVar()
    self.play_dict = {'2 players': 2,
                      '3 players': 3,
                      '4 players': 4}

    pof = LabelFrame(self.opt_cont, bg='azure', pady=10, padx=10)
    pof.pack()

    for k, v in self.play_dict.items():
      r = Radiobutton(pof, bg='azure', text=k, variable=self.play_var, value=v)
      r.pack(anchor=NW)

    self.play_var.set(2)

  def construct_options(self):
    self.options = {}
    self.options['names'] = [self.name_var.get()]
    self.options['lan_mode'] = True
    self.options['time_limit'] = self.time_var.get()
    self.options['play_num'] = self.play_var.get()
    self.options['chal_mode'] = bool(self.chal_var.get())
    self.options['point_limit'] = self.point_var.get()

    self.parent.master.set_geometry()

    self.parent.master.child = GamePage(self.parent, self.options)

    self.destroy()

############################################################################

class NormalStartPage(StartPage):
  def draw_player_options(self):
    self.but_var.set('Next')

    self.play_var = IntVar()
    self.play_dict = {'2 players': 2,
                      '3 players': 3,
                      '4 players': 4}

    pof = LabelFrame(self.opt_cont, bg='azure', pady=10, padx=10)
    pof.pack()

    for k, v in self.play_dict.items():
      r = Radiobutton(pof, bg='azure', text=k, variable=self.play_var, value=v)
      r.pack(anchor=NW)

    self.play_var.set(2)

  def draw_name_fields(self):
    self.parent.master.geometry('704x500')
    self.parent.master.minsize(704, 500)

    t = Frame(self, pady=20, padx=10, bg='azure')
    t.pack()

    for p in range(1, self.play_var.get() + 1):
      var = StringVar()

      f = Frame(t, bg='azure')
      f.pack(side=TOP)

      Label(f, text='Enter Player {}\'s name:'.format(p), bg='azure').pack(side=LEFT)

      ent = Entry(f, textvariable=var)
      ent.pack(side=LEFT)

      if p == 1:
        ent.focus_set()

      self.play_ents.append(ent)

  def get_player_names(self):
    names = []

    for name in self.play_ents:
      names.append(name.get().strip().capitalize())

    self.options = {'names': names}

    random.shuffle(self.options['names'])

  def construct_options(self):
    if self.play_ents:
      self.get_player_names()

      self.options['normal_mode'] = True
      self.options['time_limit'] = self.time_var.get()
      self.options['play_num'] = self.play_var.get()
      self.options['chal_mode'] = bool(self.chal_var.get())
      self.options['point_limit'] = self.point_var.get()

      self.parent.master.set_geometry()

      GamePage(self.parent, self.options, self.dict)

      self.destroy()
    else:
      self.draw_name_fields()

      self.but_var.set('Start Game')