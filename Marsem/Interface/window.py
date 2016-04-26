#!/usr/bin/env python
import gtk
import pygtk
pygtk.require('2.0')

def open_file(self):
    print "Open"


def save_file(self):
    print "Save"

def quit_file(self):
    print "Quit"

def start_clicked(self):
    print "Start"


def download_clicked(self):
    print "Download"


def picture_clicked(self):
    print "Image taken"


class Menu:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", lambda wid: gtk.main_quit())
        window.connect("delete_event", lambda a1, a2: gtk.main_quit())
        window.set_title("Marsem")
        window.set_size_request(300, 200)

        file_menu = gtk.Menu()  # Don't need to show menus
        #Menu Items
        open_item = gtk.MenuItem("Open")
        save_item = gtk.MenuItem("Save")
        quit_item = gtk.MenuItem("Quit")

        file_menu.append(open_item)
        file_menu.append(save_item)
        file_menu.append(quit_item)

        #CallBack to menu items
        open_item.connect_object("activate", open_file, "file.open")
        save_item.connect_object("activate", save_file, "file.save")
        quit_item.connect_object("activate", quit_file, "file.quit")

        open_item.show()
        save_item.show()
        quit_item.show()

        menu_bar = gtk.MenuBar()
        file_item = gtk.MenuItem("File")
        file_item.show()
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)

        main_box = gtk.VBox(False, 1)
        main_box.set_border_width(1)
        window.add(main_box)
        main_box.show()

        button_box = gtk.HBox(False, 20)
        button_box.set_border_width(0)
        button_box.show()
        start_clicked
        download_clicked
        picture_clicked
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

        main_box.pack_start(menu_bar, False, True, 0)
        main_box.pack_end(button_box, False, True, 0)
        button_box.pack_start(start_button, False, False, 10)
        button_box.pack_start(download_button, False, False, 10)
        button_box.pack_end(picture_button, False, False, 10)

        button_box.show
        menu_bar.show()
        window.show()


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    Menu()
    main()
