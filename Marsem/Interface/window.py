#!/usr/bin/env python
import pygtk
import gtk
from os import listdir
from os.path import isfile, join

pygtk.require('2.0')


def picture_clicked(self):
    print"take picture"


def start_clicked(self):
    print "Start"


def download_clicked(self):
    print "Download"


# Not necessary?
def new_file(self):
    print "Creates a file"


# Not necessary?
def open_file(self):
    print "Opens a file"


# Not necessary? Change to "image path"?
def save_file(self):
    print "Saves a file"


# Not necessary?
def save_as_file(self):
    print "Saves a file as"


def options_menu(self):
    print "options"


def help_menu(self):
    print "help"


class Menu:
    def print_hello(self, w, data):
        print "Welcome to Marsem"


    def display_pictures(self):
        print "yoyo"


    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget("<main>")


    def __init__(self):
        def folder_clicked(name):
            print name


        self.menu_items = (
            ("/_File", None, None, 0, "<Branch>"),
            ("/File/_New", "<control>N", new_file(self), 0, None),
            ("/File/_Open", "<control>O", open_file(self), 0, None),
            ("/File/_Save", "<control>S", save_file(self), 0, None),
            ("/File/Save _As", None, save_as_file(self), 0, None),
            ("/File/sep1", None, None, 0, "<Separator>"),
            ("/File/Quit", "<control>Q", gtk.main_quit, 0, None),
            ("/_Options", None, options_menu(self), 0, "<Branch>"),
            ("/Options/Test", None, None, 0, None),
            ("/_Help", None, help_menu(self), 0, "<LastBranch>"),
            ("/_Help/About", None, None, 0, None),
        )

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", lambda wid: gtk.main_quit())
        window.connect("delete_event", lambda a1, a2: gtk.main_quit())
        window.set_title("Marsem")
        window.set_size_request(600, 400)

        main_box = gtk.VBox(False, 1)
        main_box.set_border_width(1)
        window.add(main_box)
        main_box.show()

        # Adding the menu bar.
        menubar = self.get_main_menu(window)
        main_box.pack_start(menubar, False, True, 0)
        menubar.show()

        # Adding picture area.
        picture_header = gtk.Label("Taken picture sets below:")
        picture_header.set_size_request(width=100, height=20)

        # TODO! Prompt user to select path upon app start.
        picture_path = '/Users/MTs/MARSEM'
        picture_folders = [folder for folder in listdir(picture_path) if not isfile(join(picture_path, folder))]

        picture_box = gtk.VBox(False, 1)
        picture_box.set_border_width(1)
        picture_box.show()
        main_box.pack_start(picture_box)

        picture_box.pack_start(picture_header)

        print(picture_folders)

        def create_button(name):
            new_button = gtk.Button(label = str(name), stock=None)
            new_button.connect("clicked", lambda e: folder_clicked(name))
            return new_button

        for folder in picture_folders:
            picture_box.pack_start(create_button(str(folder)))

        picture_box.show_all()


        # Start button
        start_button = gtk.Button(label="Start", stock=None)
        start_button.connect("clicked", start_clicked)
        start_button.set_size_request(width=70, height=20)
        start_button.show()

        # Download button
        download_button = gtk.Button(label="Download", stock=None)
        download_button.connect("clicked", download_clicked)
        download_button.set_size_request(width=70, height=20)
        download_button.show()

        # Take picture
        picture_button = gtk.Button(label="Take image", stock=None)
        picture_button.connect("clicked", picture_clicked)
        picture_button.set_size_request(width=90, height=20)
        picture_button.show()

        button_box = gtk.HBox(False, 20)
        button_box.set_border_width(0)
        button_box.show()

        button_box.pack_start(start_button, False, False, 10)
        button_box.pack_start(download_button, False, False, 10)
        button_box.pack_end(picture_button, False, False, 10)
        main_box.pack_end(button_box, False, True, 0)

        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    Menu()
    main()
