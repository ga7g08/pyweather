from setuptools import setup


setup(name='pyweather',
      packages=[''],
      version='1.0',
      entry_points={
          'console_scripts': [
              'forecast = forecast:main'
          ]
      }
      )
