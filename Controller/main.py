from logging import root
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk


w = 500
h = 450

LARGE_FONT= ('Calibri', 25)


# Set which directory to save downloaded picture sets in.
def setDirectory():
    print('Set up where picture sets will be saved')
    filedialog.askdirectory()


# Send go ahead signal to Pi to start picture taking sequence.
def startPictureTaking():
    print('Send shit to Pi')


def aboutAuthors():
    print('Stuff about author')
    infoWindow = Toplevel(root)
    infoWindow.title('About Authors')
    infoWindow.lift(root)

    info = Text(infoWindow, width=40, height=10).pack()


# Popup window when Pi sends a signal that picture sequence has ended.
def askWhenFinished():
    if messagebox.askyesno(title='Finished', message='Would you like to download the picture?') == True:
        print('You pressed yes')
    else:
        print('You pressed no')


# Function to download taken pictures.
def downloadPictureSet():
    print('Download currently selected picture set')


# Ability to browse picture sets on the Pi to download them.
def browsePictureSetsOnPi():
    print('Show all folders with pictures on PI, to be able to download older content that has not been downloaded')


class Window:
    def __init__(self, master):
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        master.resizable(FALSE, FALSE)
        master.attributes('-topmost', True)
        master.wm_title('MARSEM - Miraculously Autonomous Rover Search Environment Mapper')
        master.option_add('*tearOff', False)
        master.lift()

        tk.Label(master, text='MARSEM Control System', background='midnight blue', foreground='White', width=w, height=1, font=LARGE_FONT).pack(side=TOP, fill=X)

        self.frame_library = tk.Frame(master, width=w/4.5, height=h)
        self.frame_library.pack(side=LEFT)
        self.frame_library.pack_propagate(0)
        tk.Label(master, background='dark grey').pack(side=LEFT, fill=Y)
        self.frame_main = tk.Frame(master, width=w-(w/4.5), height=h)
        self.frame_main.pack(side=LEFT)
        self.frame_main.pack_propagate(0)

        ttk.Button(self.frame_main, text='Start', style='TButton').pack()
        progress = ttk.Progressbar(self.frame_main).pack()
        ttk.Button(self.frame_main, text='Download').pack()
        download = ttk.Progressbar(self.frame_main).pack()
        ttk.Button(self.frame_library, text='test').pack()

        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.settings = Menu(self.menu)
        self.about = Menu(self.menu)
        self.help_ = Menu(self.menu)

        self.menu.add_cascade(menu=self.settings, label='Settings')
        self.settings.add_command(label='Choose Directory', command = lambda: setDirectory())

        self.menu.add_cascade(menu=self.about, label='Authors')
        self.about.add_command(label='About authors', command = lambda: aboutAuthors())

        self.menu.add_cascade(menu=self.help_, label='Help')
        self.help_.add_command(label='Stuff')


def main():
    root = Tk()
    window = Window(root)

    root.mainloop()


if __name__ == "__main__": main()
