from tkinter import *

class EntryPage(Frame):
  def __init__(self, parent, controller):
    Frame.__init__(self, parent, bg='azure')

    self.controller = controller
    controller.geometry("704x420")
    self.draw()

  def draw(self):
    Label(self, text='Welcome to PyScrabble', font=('times', 40, 'italic'), bg='azure', pady=100).pack(side=TOP)

    f = Frame(self, bg='azure')
    f.pack(side=TOP)

    Button(f, text='Start Computer Game', command=lambda: self.go_to_frame('CompStartPage')).pack(side=LEFT, padx=10)
    Button(f, text='Start Game on Computer', command=lambda: self.go_to_frame('NormalStartPage')).pack(side=LEFT, padx=10)
    Button(f, text='Start Game on LAN', command=lambda: self.go_to_frame('LANStartPage')).pack(side=LEFT, padx=10)

    Button(self, text='Load Game').pack(side=TOP, pady=30)

  def go_to_frame(self, frame):
    self.controller.show_frame(frame)