from tkinter import *

class SideFrame(Frame):
  def __init__(self, fside, arange, parent=None, **options):
    Frame.__init__(self, parent, bg='azure', **options)
    self.pack(side=fside)
    if fside == TOP or fside == BOTTOM:
      h = 1
      w = 4
      lside = LEFT

      Label(self, bd=0, bg='azure', height=h, width=2, relief=RIDGE).pack(side=LEFT)
      Label(self, bd=0, bg='azure', height=h, width=2, relief=RIDGE).pack(side=RIGHT)
    else:
      lside = TOP
      h = 2
      w = 2

    com = str if 1 in arange else chr

    for i in arange:
      label = Label(self, text=com(i))
      label.config(bd=1, height=h, width=w, bg='dark gray', fg='white',relief=RIDGE)
      label.pack(side=lside)
