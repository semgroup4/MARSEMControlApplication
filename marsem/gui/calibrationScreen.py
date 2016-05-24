#!/usr/bin/python3.4 -tt
# -*- coding: utf-8 -*-

import marsem.protocol.car as car
from marsem.opencv import Color
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image as KivyImage
from kivy.lang import Builder

from PIL import Image

import numpy

Builder.load_file("calibrationScreen.kv")


class CalibrationScreen(Screen):

    color = Color()

    # Grabs an image from the camera and saves to file
    def update_picture(self):

        if(False): # TODO - Check if camera is available to prevent hanging
            new_pic = car.picture()
        else:
            new_pic = numpy.fromfile('unavailable.jpg', dtype='int16', sep="")

        print("Worked")
        file = open('calibImage.jpg','wb+')
        file.write(new_pic)

    # Returns a pretty string of the color range
    def get_color_string(self):
        return 'Min: ' + self.color.min.__str__() + '\nMax: ' + self.color.max.__str__()

    # Returns the pixel at x, y on the calibImage
    def get_pixel_at(self, x, y):
        im = Image.open('calibImage.jpg')
        if(x >= im.width or y >= im.height or x < 0 or y < 0):
            print("Invalid pixel coordinate")
            return

        return im.getpixel((x, y))

    # Returns the selected color range
    def get_color(self):
        pass
