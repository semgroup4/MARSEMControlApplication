#!/usr/bin/env python3.4

from distutils.core import setup, find_packages

setup(name='marsem',
      version='0.1',
      description='marsem Control Application',
      author='Group 4',
      url='https://github.com/semgroup4/MARSEMControlApplication',
      packages=find_packages("marsem", exclude=["test"]),
)
