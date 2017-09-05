from tkinter import *
from start_page import CompStartPage, NormalStartPage, LANStartPage
from game_page import GamePage
from entry_page import EntryPage

class Root(Tk):
  def __init__(self):
    Tk.__init__(self)
    self.title('PyScrabble')

    self.container = Frame(self, bg='azure')
    self.container.pack(side=TOP, fill=BOTH, expand=YES)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    self.draw_menu()
    self.construct_frames()

  def construct_frames(self):
    self.frames = {}

    for F in (EntryPage, CompStartPage, NormalStartPage, LANStartPage, GamePage):
      page_name = F.__name__
      f = F(parent=self.container, controller=self)
      self.frames[page_name] = f
      f.grid(row=0, column=0, sticky=S+N+E+W)

    self.show_frame('EntryPage')

  def deconstruct_frames(self):
    for k, v in self.frames.items():
      v.destroy()

  def draw_menu(self):
    top = Menu(self)
    self.config(menu=top)

    game_m = Menu(top)
    game_m.add_command(label='New Game', underline=0, command=self.go_to_beginning)
    game_m.add_command(label='Load Game', underline=0)
    game_m.add_command(label='Quit', underline=0, command=self.quit)

    top.add_cascade(label='Game', menu=game_m, underline=0)

  def show_frame(self, page_name):
    f = self.frames[page_name]
    f.tkraise()

  def go_to_beginning(self):
    self.geometry("704x420")
    self.deconstruct_frames()
    self.construct_frames()


Root().mainloop()
