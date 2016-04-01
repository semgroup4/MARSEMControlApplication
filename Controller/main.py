from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

root = Tk()

w = 800
h = 650

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.wm_title('MARSEM - Miraculously Autonomous Rover Search Environment Mapper')

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

panedWindow = ttk.PanedWindow(root, orient = HORIZONTAL)
panedWindow.pack(fill = BOTH, expand = True)

framepictureset = ttk.Frame(panedWindow, width = 100, height = 300, relief = SUNKEN)
framemain = ttk.Frame(panedWindow, width = 300, height = 300, relief = SUNKEN)

panedWindow.add(framepictureset, weight = 0)
panedWindow.add(framemain, weight = 1)

# Set which directory to save downloaded picture sets in.
def setdirectory():
    print 'Set up where picture sets will be saved'


# Send go ahead signal to Pi to start picture taking sequence.
def startpicturetaking():
    print 'Send shit to Pi'


# Popup window when Pi sends a signal that picture sequence has ended.
def askwhenfinished():
    if messagebox.askyesno(title = 'Finished', message = 'Would you like to download the picture?') == True:
        print 'You pressed yes'
    else:
        print 'You pressed no'


# Function to download taken pictures.
def downloadpictureset():
    print 'Download currently selected picture set'


# Ability to browse picture sets on the Pi to download them.
def browsepicturesetsonpi():
    print 'Show all folders with pictures on PI, to be able to download older content that has not been downloaded'


root.option_add('*tearOff', False)
menubar = Menu(root)
root.config(menu = menubar)

settings = Menu(menubar)
menubar.add_cascade(menu = settings, label = 'Settings')
settings.add_command(label = 'Directory to save in', command = setdirectory)

help_ = Menu(menubar)
menubar.add_cascade(menu = help_, label = 'Help')
help_.add_command(label = 'Stuff')

about = Menu(menubar)
menubar.add_cascade(menu = about, label = 'About')
about.add_command(label = 'Developers')


btnstart = ttk.Button(framemain, text = 'Start', command = startpicturetaking).pack()
progresspictures = ttk.Progressbar(framemain).pack()


btndownload = ttk.Button(framemain, text = 'Download', command = downloadpictureset).pack()
progressdownload = ttk.Progressbar(framemain).pack()


root.mainloop()
