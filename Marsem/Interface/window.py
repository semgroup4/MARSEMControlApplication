#!/usr/bin/env python
import pygtk

pygtk.require('2.0')
import gtk

def picture_clicked(self):
    print"take picture"

def start_clicked(self):
    print "Start"


def download_clicked(self):
    print "Download"


def new_file(self):
    print "Creates a file"


def open_file(self):
    print "Opens a file"


def save_file(self):
    print "Saves a file"


def save_as_file(self):
    print "Saves a file as"


def options_menu(self):
    print "options"


def help_menu(self):
    print "help"


class Menu:
    def print_hello(self, w, data):
        print "Welcome to Marsem"

    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget("<main>")


    def __init__(self):
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
        window.set_size_request(300, 200)

        main_box = gtk.VBox(False, 1)
        main_box.set_border_width(1)
        window.add(main_box)
        main_box.show()

        button_box = gtk.HBox(False, 20)
        button_box.set_border_width(0)
        window.add(button_box)
        button_box.show()
        menubar = self.get_main_menu(window)

        # Buttons
        # Start
        start_button = gtk.Button(label="Start", stock=None)
        start_button.connect("clicked", start_clicked)
        start_button.set_size_request(width=70, height=20)
        start_button.show()
        # Download
        download_button = gtk.Button(label="Download", stock=None)
        download_button.connect("clicked", download_clicked)
        download_button.set_size_request(width=70, height=20)
        download_button.show()
        # Pictures
        picture_button = gtk.Button(label="Take image", stock=None)
        picture_button.connect("clicked", picture_clicked)
        picture_button.set_size_request(width=90, height=20)
        picture_button.show()

        main_box.pack_start(menubar, False, True, 0)
        main_box.pack_end(button_box, False, True, 0)
        button_box.pack_start(start_button, False, False, 10)
        button_box.pack_start(download_button, False, False, 10)
        button_box.pack_end(picture_button, False, False, 10)

        button_box.show
        menubar.show()
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    Menu()
    main()
