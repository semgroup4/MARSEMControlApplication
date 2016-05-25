#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.protocol.car as car
from marsem.opencv import Color
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
import io


from PIL import Image

import numpy

Builder.load_file("calibrationScreen.kv")


# Currently writes the snapshot to file, but it may be cleaner
# to simply store the data in a variable.
class CalibrationScreen(Screen):
   
    color = Color()

    color_string = StringProperty()
    current_action_string = StringProperty()

    # NOTE:
    # The pixel selector is extremely hacky and relies on hardcoded
    # image position values. These values must be adjusted if the UI
    # layout is at all modified.
    image_dimensions = 420, 340
    image_offset = 50, 50

    # Selection action for min/max colors: -1 none, 0 min, 1 max
    selection = -1

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

        return 'calibImage.jpg'

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

        # Normalized position on the image
        normalized_pos = [touch.x - self.image_offset[0], touch.y - self.image_offset[1]]
        normalized_pos[0] = normalized_pos[0] / self.image_dimensions[0]
        normalized_pos[1] = normalized_pos[1] / self.image_dimensions[1]

        # Check if image was clicked and selection in progress
        if(self.selection == -1 or
                   normalized_pos[0] > 1 or normalized_pos[0] < 0 or
                   normalized_pos[1] > 1 or normalized_pos[1] < 0):
            self.selection = -1
            return

        img = Image.open('calibImage.jpg')

        img_x = normalized_pos[0] * img.width
        img_y = normalized_pos[1] * img.height
        # Flip y so down is +
        img_y = img.height - img_y

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
