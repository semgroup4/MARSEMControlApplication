import os
import sys
import time

from os.path import join


# Config is loaded upon each application start and contains information that the application needs to function
# properly. All available settings can be reached from other files by referencing the SETTINGS list. Settings are
# first loaded through a text file and then input to the SETTINGS list.
#
# Author:

# List containing all available settings for the application.
SETTINGS = []


def initialize():
    # Check if settings file exists to avoid errors.
    if os.path.exists(join(sys.path[0], "settings.txt")):
        try:
            with open(join(sys.path[0], "settings.txt"), "r") as file:
                # Temporary storage for settings before they are pushed to global variable.
                tmp_settings = []

                # Read the opened file line by line into a list.
                for line in file:
                    # Getting rid of those pesky new lines when settings are read from the file.
                    tmp_settings.append(line.rstrip('\n'))

                # Read settings without fuss into global list. Removing all content before each '='
                for setting in tmp_settings:
                    # Settings are read from AFTER the equals sign to remove any unwanted stuff. Index the '=' and plus 1.
                    SETTINGS.append(setting[setting.index("=") + 1:])
        except IOError or ValueError:
            print('Program settings file could not be loaded.')
    else:
        # No settings file was found, a new and fresh one is created.
        with open(join(sys.path[0], "settings.txt"), "w") as new_settings:
            new_settings.write("picture_path=\n")


# When the user wishes to change the path to save pictures in, here is where they end up.
def change_picture_path(new_path):
    # First, create a new .txt file to read the changes into. Keeping the original in case something goes wrong.
    with open(join(sys.path[0], "settings.txt.tmp"), "w") as tmp_settings:
        tmp_settings.write("picture_path=" + new_path + "\n")
        os.rename("settings.txt.tmp", "settings.txt")

    # The existing settings list needs to be updated too since it is loaded upon program start and has the old value.
    initialize()

# Calling initialize upon .py import to gather settings into SETTINGS-list.
initialize()