#!/usr/bin/env python
import pygtk
import gtk
from os import listdir
from os.path import isfile, join
pygtk.require('2.0')

main_box = gtk.VBox(False, 40)
main_box.set_border_width(1)
main_box.show()


def start_clicked(self):
    print "Start"


def open_file(self):
    chooser = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                    buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    chooser.set_default_response(gtk.RESPONSE_OK)

    open_filter = gtk.FileFilter()
    open_filter.set_name("Images")
    open_filter.add_mime_type("image/png")
    open_filter.add_mime_type("image/jpeg")
    open_filter.add_mime_type("image/gif")
    open_filter.add_pattern("*.jpg")
    chooser.add_filter(open_filter)

    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        print chooser.get_filename(), 'selected'
    elif response == gtk.RESPONSE_CANCEL():
        print 'Closed, you did not choose any files'
    chooser.destroy()


def save_as_file(self):
    chooser = gtk.FileChooserDialog(title=None, action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                    buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    new_filter = gtk.FileFilter()
    new_filter.set_name("Images")
    new_filter.add_mime_type("image/png")
    new_filter.add_mime_type("image/jpeg")
    new_filter.add_mime_type("image/gif")
    new_filter.add_pattern("*.jpg")
    chooser.add_filter(new_filter)
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        print chooser.get_filename(), 'selected'
    elif response == gtk.RESPONSE_CANCEL():
        print 'Closed, you did not choose any files'

    chooser.destroy()


def quit_file(self):
    gtk.main_quit()
    print "Quit"


def start_clicked(self):
    print "Start"


def download_clicked(self):
    print "Download"


def display_pictures(self):
    print "yoyo"


def picture_clicked(self):
    print "Image taken"


def folder_clicked(folder_name):
    print folder_name


"""

Main class, when called it created the entire Application.

"""


class Marsem:

    def __init__(self):

        container = gtk.Window(gtk.WINDOW_TOPLEVEL)
        container.connect("destroy", lambda wid: gtk.main_quit())
        container.connect("delete_event", lambda a1, a2: gtk.main_quit())
        container.set_title("Marsem")
        container.set_size_request(600, 400)

        container.add(main_box)
        container.show()


"""

The menu class creates a menu with the specified items below. Getter for inserting the menu anywhere available.

"""


class Menu:

    def __init__(self):
        # HBox to add finished menu to.
        self.menu_box = gtk.VBox(False, 0)
        self.menu_box.set_border_width(0)
        self.menu_box.show()

        # Create menu.
        self.file_menu = gtk.Menu()

        # Create menu items.
        open_item = gtk.MenuItem("Open")
        save_item = gtk.MenuItem("Save")
        quit_item = gtk.MenuItem("Quit")
        open_item.connect_object("activate", open_file, "file.open")
        save_item.connect_object("activate", save_as_file, "file.save")
        quit_item.connect_object("activate", quit_file, "file.quit")
        self.file_menu.append(open_item)
        self.file_menu.append(save_item)
        self.file_menu.append(quit_item)
        open_item.show()
        save_item.show()
        quit_item.show()

        # Create menu bar to display menu items.
        self.menu_bar = gtk.MenuBar()
        file_item = gtk.MenuItem("File")
        file_item.show()
        file_item.set_submenu(self.file_menu)
        self.menu_bar.append(file_item)
        self.menu_bar.show()

        # Pack created menu into box.
        self.menu_box.pack_start(self.menu_bar, False, False, 0)
        main_box.pack_start(self.menu_box, False, False, 0)


"""

Handling pictures, both listing folders available (containing picture sets) but also provides a function to display
all pictures of a clicked folder inside the application.

"""


class PictureHandler:

    def __init__(self):

        # VBox to add picture set buttons to.
        picture_box = gtk.VBox(False, 0)
        picture_box.set_border_width(1)
        picture_box.show()

        # Adding info label.
        picture_header = gtk.Label("Taken picture sets below:")
        picture_header.set_size_request(width=100, height=20)
        picture_box.pack_start(picture_header)

        # TODO: Prompt user to specify image path once.
        # Path to image sets.
        picture_path = '/Users/MTs/MARSEM'

        # For each folder found, create an entry in list.
        picture_folders = [folder
                           for folder in listdir(picture_path) if not isfile(join(picture_path, folder))]

        # Definition for creating buttons per folder found in path.
        def create_button(name):
            new_button = gtk.Button(label=str(name), stock=None)
            # Each time a button is clicked, the folder_clicked function is called with the folder-buttons name.
            new_button.connect("clicked", lambda e: folder_clicked(name))
            return new_button

        # Loop for creating one button per image set folder. Calling the definition above.
        for folder in picture_folders:
            picture_box.pack_start(create_button(str(folder)))

        # Show everything that has been packed into picture_box.
        picture_box.show_all()

        # Final pack into main_box to show in open window.
        main_box.pack_start(picture_box, False, False, 10)


class Buttons:

    def __init__(self):
        
        # Hbox for adding all funcionality buttons to the window.
        button_box = gtk.HBox(False, 20)
        button_box.set_border_width(0)
        button_box.show()

        # Creating the buttons:
        start_button = gtk.Button(label="Start", stock=None)
        start_button.set_size_request(width=70, height=20)
        start_button.connect("clicked", start_clicked)

        download_button = gtk.Button(label="Download", stock=None)
        download_button.connect("clicked", download_clicked)
        download_button.set_size_request(width=70, height=20)

        picture_button = gtk.Button(label="Take image", stock=None)
        picture_button.connect("clicked", picture_clicked)
        picture_button.set_size_request(width=90, height=20)

        # TODO: Research more about coloring widgets.
        #map = start_button.get_colormap()
        #color = map.alloc_color("blue")

        # copy the current style and replace the background
        # style = start_button.get_style().copy()
        # style.bg[gtk.STATE_NORMAL] = color

        # set the button's style to the one you created
        # start_button.set_style(style)

        # Packing created buttons into button_box.
        button_box.pack_start(start_button, False, False, 5)
        button_box.pack_start(download_button, False, False, 0)
        button_box.pack_end(picture_button, False, False, 5)

        # Show all packed widgets.
        button_box.show_all()

        # Insert button_box into main_box for displaying everything in the open window.
        main_box.pack_start(button_box, False, False, 5)


# Main loop of the application.
def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    # The order of class names below determines where in the window they will be inserted. Adding menu last will place
    # the menu bar at the bottom of the screen.
    Menu()
    PictureHandler()
    Buttons()
    Marsem()
    main()
