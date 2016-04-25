import gtk
import pygtk


class Base:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()

    def main(self):
        gtk.main()


def start_clicked(self):
    print "Start"


def download_clicked(self):
    print "Download"


if __name__ == "__main__":
    box = gtk.HBox(False, 0)
    b1 = gtk.Button(label="Start", stock=None)
    b1.connect("clicked", start_clicked)
    b2 = gtk.Button(label="Download", stock=None)
    b2.connect("clicked", download_clicked)
    box.show()
    b1.show()
    b2.show()
    base = Base()
    box.add(b1)
    box.add(b2)
    base.window.add(box)
    base.main()
