#!/usr/bin/env python3.4

from setuptools import setup, find_packages

setup(name='Marsem_control',
      version='1.0',
      description='Marsem Control Application',
      author='Group 4',
      url='https://github.com/semgroup4/MARSEMControlApplication',
      packages=find_packages(exclude=["test"]),
      package_data = {
          'marsem': ['*.kv'],
      },
      entry_points={
          'gui_scripts': [
              'main = marsem.gui',
          ]
      },
)
