from tkinter import *

class PlayerNamePopup(Toplevel):
  def __init__(self, parent, player_num, options, controller):
    Toplevel.__init__(self, parent)
    self.player_num = player_num + 1
    self.options = options
    self.controller = controller
    self.players = []
    self.draw_name_fields()
    Button(self, text='Submit', command=self.get_player_names).pack(side=BOTTOM)

  def draw_name_fields(self):
    for p in range(1, self.player_num):
      var = StringVar()
      f = Frame(self)
      f.pack(side=TOP)
      Label(f, text='Enter Player {}\'s name:'.format(p)).pack(side=LEFT)
      ent = Entry(f, textvariable=var)
      ent.pack(side=LEFT)
      self.players.append(ent)

  def get_player_names(self):
    names = []
    for name in self.players:
      names.append(name.get())

    self.options['names'] = names
    self.destroy()
    self.controller.show_frame('GamePage')