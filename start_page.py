from tkinter import *

class StartPage(Frame):
  def __init__(self, parent, controller, **options):
    Frame.__init__(self, parent, bg='azure', **options)

    self.controller = controller

    self.chal_var = IntVar()
    self.time_var = IntVar()
    self.but_var = StringVar()

    self.but_var.set('Start Game')

    self.options = {}
    self.players = []

    self.draw_heading()
    self.draw_buttons()
    self.draw_player_name()

    self.opt_cont = Frame(self, bg='azure')
    self.opt_cont.pack(side=TOP, padx=96)

    self.draw_player_options()
    self.draw_secondary_options()

  def draw_heading(self):
    Label(self, text='OPTIONS', font=('times', 35, 'italic'), bg='azure', pady=40).pack(side=TOP)

  def draw_secondary_options(self):
    sof = LabelFrame(self.opt_cont, bg='azure', padx=50, pady=10)
    sof.pack(side=LEFT)

    cb = Checkbutton(sof, bg='azure', text='Challenge Mode', variable=self.chal_var)
    cb.pack(anchor=NW)
    cb.deselect()

    Label(sof, bg='azure', text='Time Limit:').pack(side=LEFT)

    ent = Entry(sof, textvariable=self.time_var, width=3)
    ent.pack(side=LEFT)
    ent.insert(1, 0)

  def draw_buttons(self):
    f = LabelFrame(self, bd=0, bg='azure')
    f.pack(side=BOTTOM, pady=40)
    Button(f, textvariable=self.but_var, command=self.construct_options).pack(pady=10)

  def draw_player_name(self): pass

  def draw_player_options(self): pass

  def construct_options(self): pass

#############################################################################

class CompStartPage(StartPage):
  def draw_player_name(self):
    self.name_var = StringVar()

    f = Frame(self, bg='azure')
    f.pack(side=TOP, pady=20)

    Label(f, text='Enter Your Name:', bg='azure').pack(side=LEFT)
    Entry(f, textvariable=self.name_var).pack(side=LEFT)

  def construct_options(self):
    self.options['comp_mode'] = True
    self.options['time_limit'] = self.time_var.get()
    self.options['player_name'] = self.name_var.get()
    self.options['challenge_mode'] = bool(self.chal_var.get())
    print(self.options)
    self.controller.geometry("704x772")
    self.controller.show_frame('GamePage')

#############################################################################

class LANStartPage(CompStartPage):
  def draw_player_options(self):
    self.play_var = IntVar()
    self.play_dict = {'2 players': 2,
                      '3 players': 3,
                      '4 players': 4}

    pof = LabelFrame(self.opt_cont, bg='azure', pady=10, padx=10)
    pof.pack(side=LEFT)

    for k, v in self.play_dict.items():
      r = Radiobutton(pof, bg='azure', text=k, variable=self.play_var, value=v)
      r.pack(anchor=NW)

    self.play_var.set(2)

  def construct_options(self):
    self.options['network_mode'] = True
    self.options['time_limit'] = self.time_var.get()
    self.options['player_name'] = self.play_var.get()
    self.options['players'] = self.play_var.get()
    self.options['challenge_mode'] = bool(self.chal_var.get())
    print(self.options)
    self.controller.geometry("704x772")
    self.controller.show_frame('GamePage')

#############################################################################

class NormalStartPage(StartPage):
  def draw_player_options(self):
    self.but_var.set('Next')

    self.play_var = IntVar()
    self.play_dict = {'2 players': 2,
                      '3 players': 3,
                      '4 players': 4}

    pof = LabelFrame(self.opt_cont, bg='azure', pady=10, padx=10)
    pof.pack(side=LEFT)

    for k, v in self.play_dict.items():
      r = Radiobutton(pof, bg='azure', text=k, variable=self.play_var, value=v)
      r.pack(anchor=NW)

    self.play_var.set(2)

  def draw_name_fields(self):
    self.controller.geometry("704x500")

    t = LabelFrame(self, pady=10, padx=10, bg='azure')
    t.pack(pady=10)

    for p in range(1, self.play_var.get() + 1):
      var = StringVar()
      f = Frame(t, bg='azure')
      f.pack(side=TOP)
      Label(f, text='Enter Player {}\'s name:'.format(p), bg='azure').pack(side=LEFT)
      ent = Entry(f, textvariable=var)
      ent.pack(side=LEFT)
      self.players.append(ent)

  def get_player_names(self):
    names = []
    for name in self.players:
      names.append(name.get())

    self.options['names'] = names

  def construct_options(self):
    if self.players:
      self.get_player_names()
      self.options['normal_mode'] = True
      self.options['time_limit'] = self.time_var.get()
      self.options['players'] = self.play_var.get()
      self.options['names'] = self.players
      self.options['challenge_mode'] = bool(self.chal_var.get())
      print(self.options)
      self.controller.geometry("704x772")
      self.controller.show_frame('GamePage')
    else:
      self.draw_name_fields()
      self.but_var.set('Start Game')