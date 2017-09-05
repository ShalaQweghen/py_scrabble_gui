from tkinter import *

class StartPage(Frame):
  def __init__(self, parent, controller, **options):
    Frame.__init__(self, parent, bg='azure', **options)

    self.controller = controller
    self.mode_var = IntVar()
    self.chal_var = IntVar()
    self.time_var = IntVar()
    self.play_var = IntVar()
    self.mode_dict = {'Start a game on this computer': 1,
                      'Start a game against computer': 2,
                      'Start a game on LAN': 3}
    self.play_dict = {'2 players': 2,
                      '3 players': 3,
                      '4 players': 4}
    self.options = {}
    self.draw()

  def draw_heading(self):
    Label(self, text='Welcome to PyScrabble', font=('times', 40, 'italic'), bg='azure', pady=100).pack(side=TOP)

  def draw_buttons(self):
    f = LabelFrame(self, bd=0, bg='azure')
    f.pack(side=BOTTOM, pady=60)
    Button(f, text='Start Game', command=self.construct_options).pack()
    Button(f, text='Load a Game').pack()

  def draw_options(self):
    f = Frame(self, bg='azure')
    f.pack(side=TOP, padx=96)

    pof = LabelFrame(f, bg='azure', pady=10, padx=10)
    pof.pack(side=BOTTOM)

    for k, v in self.play_dict.items():
      r = Radiobutton(pof, bg='azure', text=k, variable=self.play_var, value=v)
      r.pack(anchor=NW)

    self.play_var.set(2)

    mof = LabelFrame(f, padx=30, bg='azure')
    mof.pack(side=LEFT)

    for k, v in self.mode_dict.items():
      r = Radiobutton(mof, bg='azure', text=k, variable=self.mode_var, value=v)
      r.pack(anchor=NW)

    self.mode_var.set(1)

    sof = LabelFrame(f, padx=50, pady=10, bg='azure')
    sof.pack(side=LEFT)

    cb = Checkbutton(sof, bg='azure', text='Challenge Mode', variable=self.chal_var)
    cb.pack(anchor=NW)
    cb.deselect()

    Label(sof, bg='azure', text='Time Limit:').pack(side=LEFT)

    ent = Entry(sof, textvariable=self.time_var, width=3)
    ent.pack(side=LEFT)
    ent.insert(1, 0)

  def draw(self):
    self.draw_heading()
    self.draw_buttons()
    self.draw_options()


  def set_mode(self):
    mode = self.mode_var.get()

    if mode == 1:
      self.options['normal_mode'] = True
      self.options['computer_mode'] = False
      self.options['lan_mode'] = False
    elif mode == 2:
      self.options['normal_mode'] = False
      self.options['computer_mode'] = True
      self.options['lan_mode'] = False
    else:
      self.options['normal_mode'] = False
      self.options['computer_mode'] = False
      self.options['lan_mode'] = True

  def construct_options(self):
    self.set_mode()
    self.options['time_limit'] = self.time_var.get()
    self.options['player'] = self.play_var.get()
    self.options['challenge_mode'] = bool(self.chal_var.get())
    print(self.options)
    self.controller.show_frame('GamePage')