from tkinter import *
from start_page import StartPage
from game_page import GamePage

class Root(Tk):
  def __init__(self):
    Tk.__init__(self)
    self.title('PyScrabble')
    self.minsize(704, 772)

    self.draw_menu()

    container = Frame(self, bg='azure')
    container.pack(side=TOP, fill=BOTH, expand=YES)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}

    for F in (StartPage, GamePage):
      page_name = F.__name__
      f = F(parent=container, controller=self)
      self.frames[page_name] = f
      f.grid(row=0, column=0, sticky=S+N+E+W)

    self.show_frame('StartPage')

  def draw_menu(self):
    top = Menu(self)
    self.config(menu=top)

    game_m = Menu(top)
    game_m.add_command(label='New Game', underline=0, command=(lambda: self.show_frame('StartPage')))
    game_m.add_command(label='Load Game', underline=0)
    game_m.add_command(label='Quit', underline=0, command=self.quit)

    top.add_cascade(label='Game', menu=game_m, underline=0)

  def show_frame(self, page_name):
    f = self.frames[page_name]
    f.tkraise()


Root().mainloop()
