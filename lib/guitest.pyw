from tkinter import *
from tkinter.messagebox import *
from tile import BoardTile, RackTile
from side_frame import SideFrame

def notdone():
  showerror('Not implemented', 'Not yet available')

root = Tk()

top = Menu(root)
root.config(menu=top)

file = Menu(top)

submenu = Menu(file, tearoff=True)
submenu.add_command(label='With Comp', command=notdone, underline=0)
submenu.add_command(label='On This Computer', command=notdone, underline=0)
submenu.add_command(label='On LAN', command=notdone, underline=0)
file.add_cascade(label='New Game', menu=submenu, underline=0)

file.add_command(label='Load Game', command=notdone, underline=0)
file.add_command(label='Quit', command=root.quit, underline=0)
top.add_cascade(label='Game', menu=file, underline=0)

boardoutframe = Frame(root)
boardoutframe.pack()

SideFrame(TOP, range(97, 112), boardoutframe)
SideFrame(BOTTOM, range(97, 112), boardoutframe)
SideFrame(LEFT, range(1, 16), boardoutframe)
SideFrame(RIGHT, range(1, 16), boardoutframe)

boardframe = Frame(boardoutframe)
boardframe.pack()

start = None

def handleEvent(event):
  global start

  start_name = type(start).__name__
  widget_name = type(event.widget).__name__
  widget_var = event.widget.var

  if start_name == 'RackTile' and start.var.get() != '':
    if widget_name == 'BoardTile':
      if widget_var.get() == '':
        widget_var.set(start.var.get())
        start.var.set('')
        start = None
    elif widget_name == 'RackTile':
      temp = widget_var.get()
      widget_var.set(start.var.get())
      start.var.set(temp)
      start = None
    else:
      start = None
  elif start_name == 'BoardTile' and start.var.get() != '':
    if widget_name == 'RackTile' and widget_var.get() == '':
      widget_var.set(start.var.get())
      start.var.set('')
      start = None
    elif widget_name == 'BoardTile' and widget_var.get() == start.var.get():
      start = None
  else:
    start = event.widget

c = range(97, 112)
r = range(1, 16)
row = 0
while row < 15:
  col = 0
  while col < 15:
    t = BoardTile(row, col, boardframe)
    t.bind('<1>', handleEvent)
    col += 1
  row += 1

rack = Frame(root)
rack.pack()

for i in range(7):
  t = RackTile(rack, str(i))
  t.bind('<1>', handleEvent)


root.title('PyScrabble')
root.config(height=1000, width=1000)
root.mainloop()

