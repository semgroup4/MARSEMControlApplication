#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import numpy
import io

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from kivy.lang import Builder

from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.metrics import dp

import marsem.protocol.car as car
from marsem.opencv import Color

from PIL import Image


Builder.load_file("calibrationScreen.kv")


# Globally accessible, needs to be this way!
CURRENT_COLOR = Color()


# Currently writes the snapshot to file, but it may be cleaner
# to simply store the data in a variable.
class CalibrationScreen(Screen):
    # Selection action for min/max colors: -1 none, 0 min, 1 max
    selection = -1

    # String propertys that are linked to one label each to display values.
    color_string = StringProperty('N/A')
    current_action_string = StringProperty('No action selected')

    r_min = NumericProperty(0)
    g_min = NumericProperty(0)
    b_min = NumericProperty(0)
    r_max = NumericProperty(0)
    g_max = NumericProperty(0)
    b_max = NumericProperty(0)

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
        image = car.picture()

        if image != False:
            new_pic = image
        else:
            print ("Could not connect to camera")
            new_pic = numpy.fromfile('unavailable.jpg', dtype='int8', sep="")

        file = open('calibImage.jpg','wb+')
        file.write(new_pic)
        file.close()

    # Updates the color label with new values
    def update_color_string(self):
        self.color_string = CURRENT_COLOR.get_color()

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
        # we're calculating based on 0-1 where 1 is 100%. If self.selection is -1, no selection was made and
        # nothing happens.
        if(self.selection == -1 or
                normalized_pos[0] > 1 or normalized_pos[0] < 0 or
                normalized_pos[1] > 1 or normalized_pos[1] < 0):
            # Selection is not turned on OR the user clicked outside the image. Do NADA!
            return

        # Open the image that was clicked, we're gonna get them pesky pixels
        img = Image.open('calibImage.jpg')

        # The percentage times the image's width and height, where da pixel at?
        img_x = normalized_pos[0] * img.width
        img_y = normalized_pos[1] * img.height
        # Invert the y coordinate inside the image:
        img_y = img.height - img_y

        # Grab color values of the clicked pixel.
        r, g, b = img.getpixel((img_x, img_y))

        # Depending on action, set min or max.
        if self.selection == 0:
            CURRENT_COLOR.set_max([b, g, r])
            self.r_min = r / 255
            self.g_min = g / 255
            self.b_min = b / 255
        if self.selection == 1:
            CURRENT_COLOR.set_min([b, g, r])
            self.r_max = r / 255
            self.g_max = g / 255
            self.b_max = b / 255

        # Resets select action.
        self.selection = -1
        self.current_action_string = 'No action selected'
        self.update_color_string()
