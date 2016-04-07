from logging import root
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk


w = 500
h = 450

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
        #master.configure(background='Blue')

        self.frame_library = tk.Frame(master, width=w/4.5, height=h, background='coral')
        self.frame_library.pack(side=LEFT)

        self.frame_main = tk.Frame(master, width=w-(w/4.5), height=h, background='cornflower blue')
        self.frame_main.pack(side=LEFT)

        tk.Button(self.frame_main, text='Start').grid(row = 5, column = 1)
        progress = ttk.Progressbar(self.frame_main).grid(row = 6, column =2 )
        tk.Button(self.frame_main, text='Download').grid(row =7 , column = 3)
        download = ttk.Progressbar(self.frame_main).grid(row =15 , column = 2)
        tk.Button(self.frame_library, text='test').grid(row =9 , column = 3)

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
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.wm_title('MARSEM - Miraculously Autonomous Rover Search Environment Mapper')
    root.resizable(FALSE, FALSE)

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    root.option_add('*tearOff', False)
    window = Window(root)

    root.mainloop()


if __name__ == "__main__": main()
