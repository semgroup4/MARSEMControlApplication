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

    def update_picture(self):

        if(False): # TODO - Check if camera is available to prevent hanging
            newPic = car.picture()
        else:
            newPic = numpy.fromfile('unavailable.jpg', dtype='int16', sep="")

        print("Worked")
        file = open('calibImage.jpg','wb+')
        file.write(newPic)