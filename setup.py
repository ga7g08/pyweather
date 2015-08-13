from setuptools import setup

setup(name='pyweather',
      packages=[''],
      version='1.0',
      install_requires=["python-forecastio", "geopy", "simplejson",
                        "colorterm"],
      entry_points={'console_scripts': ['forecast = forecast:main']}
      )
