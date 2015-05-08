from setuptools import setup
import shutil, os


setup(name='pyweather',
      packages=[''],
      version='1.0',
      entry_points={
          'console_scripts': [
              'forecast = forecast:main'
          ]
      }
      )

try:
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    src = cur_dir + "/api.txt"
    dest = "/usr/local/etc/.forecastio_apikey.txt"
    shutil.copyfile(src, dest)
except IOError:
    raise ValueError("I can't find api.txt in the local directory, please "
                     "visit https://developer.forecast.io/, register and save "
                     "the api key into a file api.txt")

