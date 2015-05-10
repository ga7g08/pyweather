from setuptools import setup
import shutil
import os


setup(name='pyweather',
      packages=[''],
      version='1.0',
      install_requires = ["python-forecastio", "geopy"],
      entry_points={'console_scripts': ['forecast = forecast:main']}
      )
