#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.protocol.car as car
from marsem.opencv import Color
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image as KivyImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.graphics import Rectangle, Point, GraphicException

from PIL import Image

import numpy

Builder.load_file("calibrationScreen.kv")


class CalibrationScreen(Screen):

    color = Color()

    # NOTE:
    # The pixel selector is extremely hacky and relies on hardcoded
    # image position values. These values must be adjusted if the UI
    # layout is at all modified.

    image_dimensions = 420, 340
    image_offset = 50, 50

    # Grabs an image from the camera and saves to file
    def update_picture(self):

        if(False): # TODO - Check if camera is available in order to prevent hanging
            new_pic = car.picture()
        else:
            new_pic = numpy.fromfile('unavailable.jpg', dtype='int16', sep="")

        file = open('calibImage.jpg','wb+')
        file.write(new_pic)

    # Returns a pretty string of the color range
    def get_color_string(self):
        return 'Min: ' + self.color.min.__str__() + \
               '\nMax: ' + self.color.max.__str__()

    # Returns the pixel at x, y on the calibImage
    def get_pixel_at(self, x, y):
        im = Image.open('calibImage.jpg')
        if(x >= im.width or y >= im.height or x < 0 or y < 0):
            print("Invalid pixel coordinate")
            return

        return im.getpixel((x, y))

    # Returns the selected color range
    def get_color(self):
        return self.color

    def on_touch_down(self, touch):
        # Normalized positions
        normalized_pos = [touch.x - self.image_offset[0], touch.y - self.image_offset[1]]
        normalized_pos[0] = normalized_pos[0] / self.image_dimensions[0]
        normalized_pos[1] = normalized_pos[1] / self.image_dimensions[1]

        # Check if image was clicked
        if(normalized_pos[0] > 1 or normalized_pos[0] < 0 or
                   normalized_pos[1] > 1 or normalized_pos[1] < 0):
            return

        img = Image.open('calibImage.jpg')

        img_x = normalized_pos[0] * img.width
        img_y = normalized_pos[1] * img.height
        # Flip y so down is +
        img_y = img.height - img_y



































