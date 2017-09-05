from tkinter import *
from tkinter.messagebox import *

from tile import BoardTile, RackTile
from side_frame import SideFrame

start = None
word = []
index = 0

def notdone():
  showerror('Not implemented', 'Not yet available')

def handleEvent(event):
  global start, word

  start_name = type(start).__name__
  widget_name = type(event.widget).__name__
  widget_var = event.widget.var

  if start_name == 'RackTile' and start.var.get() != '':
    if widget_name == 'BoardTile':
      if widget_var.get() == '':
        widget_var.set(start.var.get())
        word.append(widget_var.get())
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
      word.remove(widget_var.get())
      start.var.set('')
      start = None
    elif widget_name == 'BoardTile':
      if widget_var.get() == '':
        widget_var.set(start.var.get())
        start.var.set('')
        start = None
      elif widget_var.get() == start.var.get():
        start = None
      else:
        temp = widget_var.get()
        widget_var.set(start.var.get())
        start.var.set(temp)
        start = None
  else:
    start = event.widget


root = Tk()
root.title('PyScrabble')

top = Menu(root)
root.config(menu=top, bg='azure')

file_menu = Menu(top)

submenu = Menu(file_menu, tearoff=True)
submenu.add_command(label='With Comp', command=notdone, underline=0)
submenu.add_command(label='On This Computer', command=notdone, underline=0)
submenu.add_command(label='On LAN', command=notdone, underline=0)

file_menu.add_cascade(label='New Game', menu=submenu, underline=0)

file_menu.add_command(label='Load Game', command=notdone, underline=0)
file_menu.add_command(label='Quit', command=root.quit, underline=0)
top.add_cascade(label='Game', menu=file_menu, underline=0)

outerframe = Frame(root, padx=30, bg='azure')
outerframe.pack()

infobar = Frame(outerframe, pady=20, bg='azure')
infobar.pack(side=TOP, fill=X)

my_sc = Label(infobar, text='My Score = 15')
my_sc.config(height=2, bg='#ADFF2F', fg='#1a1a1a', padx=5)
my_sc.pack(side=LEFT, padx=13)

op_sc = Label(infobar, text='Opponent\'s Score = 115')
op_sc.config(height=2, fg='#1a1a1a', bg='#FF4500', padx=5)
op_sc.pack(side=LEFT, padx=13)

bag = Label(infobar, text='Tiles in Bag = 75')
bag.config(height=2, bg='dark gray', fg='white', padx=5)
bag.pack(side=LEFT, padx=13)

time = Label(infobar, text='Time Left = 15 min')
time.config(height=2, bg='dark gray', fg='white', padx=5)
time.pack(side=LEFT, padx=13)

SideFrame(TOP, range(97, 112), outerframe)
SideFrame(BOTTOM, range(97, 112), outerframe)
SideFrame(LEFT, range(1, 16), outerframe)
SideFrame(RIGHT, range(1, 16), outerframe)

boardframe = Frame(outerframe)
boardframe.pack()

row = 0
while row < 15:
  col = 0
  while col < 15:
    t = BoardTile(row, col, boardframe)
    t.bind('<1>', handleEvent)
    col += 1
  row += 1

rack = Frame(root, pady=15, bg='azure')
rack.pack()

for i in range(7):
  t = RackTile(rack, str(i))
  t.bind('<1>', handleEvent)


buttons = Frame(root, bg='azure')
buttons.pack()

submit = Button(buttons, text='SUBMIT', command=notdone)
submit.pack(side=LEFT, padx=5)

pas = Button(buttons, text='PASS', command=notdone)
pas.pack(side=LEFT, padx=5)

challenge = Button(buttons, text='CHALLENGE', command=notdone)
challenge.pack(side=RIGHT, padx=5)

root.update()
root.geometry()
print(root.winfo_width(), root.winfo_height())
root.minsize(root.winfo_width(), root.winfo_height() + 20)

root.mainloop()