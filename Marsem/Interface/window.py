#!/usr/bin/env python
import pygtk
import gtk
from os import listdir
from os.path import isfile, join
pygtk.require('2.0')
import gobject
import urllib
import threading

STREAM_URL = 'https://jpeg.org/images/jpeg-home.jpg'


main_box = gtk.VBox(False, 40)
main_box.set_border_width(1)
main_box.show()


def start_clicked(self):
    print "Start"


menu_box = gtk.HBox(False, 0)
menu_box.set_border_width(0)
menu_box.show()

button_box = gtk.HBox(False, 20)
button_box.set_border_width(0)
button_box.show()


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
    take_picture = gtk.Dialog(title="Take picture", parent=None, flags=0, buttons=None)
    gobject.threads_init()

    img = gtk.Image()
    img.show()

    t = VideoThread(img)
    t.start()
    take_picture.action_area.pack_start(img , True, True, 0)
    take_picture.show()
    print "Image taken"


class Window:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", lambda wid: gtk.main_quit())
        window.connect("delete_event", lambda a1, a2: gtk.main_quit())
        window.set_title("Marsem")
        window.set_size_request(600, 400)

        main_box.pack_start(menu_box, False, True, 0)
        main_box.pack_start(button_box, False, True, 0)

        window.add(main_box)
        window.show()


    def folder_clicked(name):
        print name


class Menu:
    def __init__(self):
        file_menu = gtk.Menu()
        # Menu Items
        open_item = gtk.MenuItem("Open")
        save_item = gtk.MenuItem("Save")
        quit_item = gtk.MenuItem("Quit")

        file_menu.append(open_item)
        file_menu.append(save_item)
        file_menu.append(quit_item)

        # CallBack to menu items
        open_item.connect_object("activate", open_file, "file.open")
        save_item.connect_object("activate", save_as_file, "file.save")
        quit_item.connect_object("activate", quit_file, "file.quit")

        open_item.show()
        save_item.show()
        quit_item.show()

        self.menu_bar = gtk.MenuBar()
        file_item = gtk.MenuItem("File")
        file_item.show()
        file_item.set_submenu(file_menu)
        self.menu_bar.append(file_item)
        self.menu_bar.show()

        menu_box.pack_start(self.menu_bar, False, False, 0)

        '''# Adding picture area.
        picture_header = gtk.Label("Taken picture sets below:")
        picture_header.set_size_request(width=100, height=20)

        # TODO! Prompt user to select path upon app start.
        picture_path = '/Users/Frank/MARSEM'
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
        '''

class Buttons:
    def __init__(self):
        # Buttons
        # Start
        start_button = gtk.Button(label="Start", stock=None)
        start_button.set_size_request(width=70, height=20)
        start_button.connect("clicked", start_clicked)
        start_button.show()
        # Download button
        download_button = gtk.Button(label="Download", stock=None)
        download_button.connect("clicked", download_clicked)
        download_button.set_size_request(width=70, height=20)
        download_button.show()
        # Pictures
        picture_button = gtk.Button(label="Take image", stock=None)
        picture_button.connect("clicked", picture_clicked)
        picture_button.set_size_request(width=90, height=20)
        picture_button.show()

        map = start_button.get_colormap()
        color = map.alloc_color("blue")

        # copy the current style and replace the background
        style = start_button.get_style().copy()
        style.bg[gtk.STATE_NORMAL] = color

        # set the button's style to the one you created

        start_button.set_style(style)
        button_box.pack_start(start_button, False, False, 10)
        button_box.pack_start(download_button, False, False, 0)
        button_box.pack_end(picture_button, False, False, 10)


class VideoThread(threading.Thread):

    def __init__(self, widget):
        super(VideoThread, self).__init__()
        self.widget = widget
        self.quit = False
        print 'connecting to', STREAM_URL
        self.stream = urllib.urlopen(STREAM_URL)

    def get_raw_frame(self):
        raw_buffer = ''
        while True:
            new = self.stream.read(1034)
            if not new:
                # Connection dropped
                yield None
            raw_buffer += new
            a = raw_buffer.find('\xff\xd8')
            b = raw_buffer.find('\xff\xd9')
            if a != -1 and b != -1:
                frame = raw_buffer[a:b+2]
                raw_buffer = raw_buffer[b+2:]
                yield frame

    def run(self):
        for frame in self.get_raw_frame():
            if self.quit or frame is None:
                return
            loader = gtk.gdk.PixbufLoader('jpeg')
            loader.write(frame)
            loader.close()
            pixbuf = loader.get_pixbuf()
            # Schedule image update to happen in main thread
            gobject.idle_add(self.widget.set_from_pixbuf, pixbuf)


def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    Window()
    Menu()
    Buttons()
    main()
