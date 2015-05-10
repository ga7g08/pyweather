from setuptools import setup
import shutil
import os


setup(name='pyweather',
      packages=[''],
      version='1.0',
      entry_points={
          'console_scripts': [
              'forecast = forecast:main'
          ]
      }
      )


def InstallAPIkey():
    """ Attempts methods to help install the API key for user """

    dest = "/usr/local/etc/.forecastio_apikey.txt"

    if os.path.isfile(dest):
        responce = raw_input(
            "A API key file already exists, should I just use this (y/n)\n")
        if responce in ['y', 'yes', 'Y']:
            return
        else:
            pass
    else:
        print("\nAttempting to install an API key file")

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    local_src = cur_dir + "/api.txt"
    if os.path.isfile(local_src):
        try:
            shutil.copyfile(local_src, dest)
        except IOError:
            raise ValueError(
                "Failed to copy the local_src {} to {}".format(local_src, dest)
                )
    else:
        print("No file 'api.txt' found, attempt to get the information from\n"
              "the user.")
        api_string = raw_input(
            "\nIn order to use pyweather, you need a forecast.io api key. \n"
            "Please visit www.developer.forecast.io to register, and paste "
            "your API key below:\n\n")
        if api_string.isalnum() and len(api_string) == 32:
            print("\n Installing with API key '{}'".format(api_string))
            with open(dest, "w+") as f:
                f.write(api_string)
        else:
            raise ValueError(
                "It appears the API key you have provided is of an invalid "
                "format")

InstallAPIkey()



