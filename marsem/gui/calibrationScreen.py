#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.protocol.car as car
from marsem.opencv import Color
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True

import numpy

Builder.load_file("calibrationScreen.kv")


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

    # -1 none, 0 min, 1 max
    selection = -1

    # Grabs an image from the camera and saves to file
    def update_picture(self):

        if(False): # TODO - Check if camera is available in order to prevent hanging
            new_pic = car.picture()
        else:
            new_pic = numpy.fromfile('unavailable.jpg', dtype='int16', sep="")

        file = open('calibImage.jpg','wb+')
        file.write(new_pic)
        file.close()

    # Updates the label with the color values
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

        # TODO
        # PIL has an issue with loading the file because it's truncated.
        # Despite the "Image.LOAD_TRUNCATED_IMAGES = True", which should make it load
        # the image regardless, it flat out refuses. I haven't been able to debug it
        # and it is possible it is specific only to my system.
        # I have not been able to test that the correct pixel is being grabbed
        # since the pixel function doesn't work, but it looks right.
        #
        # To enable the intended functionality, uncomment lines 90 and 97, and
        # remove the zeroed rgb assignments

        img = Image.open('calibImage.jpg')
        #img.load()

        img_x = normalized_pos[0] * img.width
        img_y = normalized_pos[1] * img.height
        # Flip y so down is +
        img_y = img.height - img_y

        #r, g, b = img.getpixel((img_x, img_y))
        r, g, b = 0, 0, 0

        if(self.selection == 0):
            self.color.set_min([r, g, b])
        if(self.selection == 1):
            self.color.set_max([r, g, b])

        self.selection = -1
        self.current_action_string = ''
        self.update_color_string()





































