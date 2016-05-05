import os
import sys
import time

from os.path import join


SETTINGS = []

# Check if settings file exists to avoid errors.
if os.path.exists(join(sys.path[0], "settings.txt")):
    try:
        settings = []
        with open(join(sys.path[0], "settings.txt"), "r") as file:
            # Read the opened file line by line into a list.
            for line in file:
                settings.append(line.rstrip('\n'))

            # Read settings without fuss into global list. Removing all content before each '='
            for item in settings:
                SETTINGS.append(item[item.index("=")+1:])
    except IOError or ValueError:
        print('Program settings file could not be loaded.')
else:
    # No settings file was found, a new and fresh one is created.
    fresh_settings = open(join(sys.path[0], "settings.txt"), "w")
    time.sleep(1)
    fresh_settings.write("picture_path=\n")
    fresh_settings.close()

print('Settings loaded: ')
for setting in SETTINGS:
    print(setting)


# When the user wishes to change the path to save pictures in, here is where they end up.
def change_picture_path(new_path):
    # First, create a new .txt file to read the changes into. Keeping the original in case something goes wrong.
    tmp_settings = open(join(sys.path[0], "settings.txt.tmp"), "w")
    tmp_settings.write("picture_path=\n")
    # TODO Complete function by writing the new path and renaming the file back to settings.txt.

    SETTINGS[0] = new_path
