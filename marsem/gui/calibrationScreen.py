#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.protocol.car as car
from marsem.opencv import Color
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.image import Image
import io
from kivy.metrics import dp


from PIL import Image

import numpy

Builder.load_file("calibrationScreen.kv")


# Currently writes the snapshot to file, but it may be cleaner
# to simply store the data in a variable.
class CalibrationScreen(Screen):
    color = Color()

    # Selection action for min/max colors: -1 none, 0 min, 1 max
    selection = -1

    # String propertys that are linked to one label each to display values.
    color_string = StringProperty('Color')
    current_action_string = StringProperty('Current action')

    def __init__(self, **kwargs):
        super(CalibrationScreen, self).__init__(**kwargs)

        # Size of the image widget (see .kv)
        self.image_dimensions = dp(500), dp(420)

    # Could not get window size in init method since the screen was not loaded yet, it just returned [100, 100]
    def get_size(self):
        self.screen_dimensions = self.size

        self.image_offset = self.screen_dimensions[0] / 2 - dp(250), self.screen_dimensions[1] / 2 - dp(210)

    # Grabs an image from the camera and saves to file
    def update_picture(self):

        # I forgot where I got the numpy.fromfile line -- maybe it's
        # not necessary at all, but it works so I won't change it.

        # Take a snapshot. If camera is not available, use placeholder image.
        if True: # TODO - Replace False with a function which checks if camera is available in order to prevent hanging
            
            new_pic = car.picture()

        else:
            print ("Could not connect to camera")
            new_pic = numpy.fromfile('unavailable.jpg', dtype='int8', sep="")

        file = open('calibImage.jpg','wb+')
        file.write(new_pic)
        file.close()

    # Updates the color label with new values
    def update_color_string(self):
        self.color_string = 'Min: ' + self.color.min.__str__() + \
               '\nMax: ' + self.color.max.__str__()

    # Returns the selected color range
    def get_color(self):
        return self.color

    # Makes the next click select the min color
    def start_select_min(self):
        self.current_action_string = 'Selecting Min'
        self.selection = 0

    # Makes the next click select the max color
    def start_select_max(self):
        self.current_action_string = 'Selecting Max'
        self.selection = 1

    # On click
    def on_touch_down(self, touch):
        super(CalibrationScreen, self).on_touch_down(touch)

        # Normalized position on the image.
        # First get the coordinates clicked, 0, 0 starts at the bottom left of the image (determined by image_offset).
        normalized_pos = [touch.x - self.image_offset[0], touch.y - self.image_offset[1]]
        # Get the location clicked IN PERCENTAGE of the image's size:
        normalized_pos[0] = normalized_pos[0] / self.image_dimensions[0]
        normalized_pos[1] = normalized_pos[1] / self.image_dimensions[1]

        # Check if image was clicked and selection in progress, basically if percentage is above 100 or below 0
        # we're calculating based on 0-1 where 1 is 100%. If self.selection is -1, no selection was to be made and
        # nothing happens.
        if(self.selection == -1 or
                normalized_pos[0] > 1 or normalized_pos[0] < 0 or
                normalized_pos[1] > 1 or normalized_pos[1] < 0):
            # Set selection back to -1 and return, do nothing!
            self.selection = -1
            return

        # Open the image that was clicked, we're gonna get them pesky pixels
        img = Image.open('calibImage.jpg')

        # The percentage times the image's width and height, where da pixel at?
        img_x = normalized_pos[0] * img.width
        img_y = normalized_pos[1] * img.height
        print(img_x)
        print(img_y)
        # Invert the y coordinate inside the image:
        img_y = img.height - img_y
        print('Second img_y: ' + str(img_y))

        # Grab color values
        r, g, b = img.getpixel((img_x, img_y))

        # Depending on action, set min or max.
        if(self.selection == 0):
            self.color.set_min([r, g, b])
        if(self.selection == 1):
            self.color.set_max([r, g, b])

        # Resets select action.
        self.selection = -1
        self.current_action_string = ''
        self.update_color_string()
