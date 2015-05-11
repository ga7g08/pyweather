import argparse
import numpy as np
import os
import shutil
import forecastio
from geopy.geocoders import Nominatim


def find_nearest(array, value):
    " Find the idx of nearest to value in array "
    idx = (np.abs(array-value)).argmin()
    return idx


def date_formatter(date):
    " Formats the x axis labels "
    return "{:02}/{:02}".format(date.month, date.day)


def print_table(xaxis, ylow, yhigh, ny=20, xlabel="Month/Year"):
    " Print ASCII table for range y1-> y2 "

    nx = len(yhigh)

    MAX = np.ceil(np.max(yhigh))
    MIN = np.floor(np.min(ylow))
    range_vals = np.linspace(MAX, MIN, ny+1)

    high_binned = [find_nearest(range_vals, val) for val in yhigh]
    low_binned = [find_nearest(range_vals, val) for val in ylow]

    yaxis = ["{:04.01f} |".format(v) if i % 2 == 0 else "     |"
             for (i, v) in enumerate(range_vals)]

    dx = 3  # Should be odd
    dx_gap = 2
    delta = dx + 2 * dx_gap
    ydata = np.array([[" " for i in range(ny+1)] for j in range(delta*nx)])

    for i, jhigh, jlow in zip(range(0, delta*nx, delta),
                              high_binned, low_binned):
        ydata[i+dx_gap:i+dx_gap+dx, jhigh] = "_"
        ydata[i+dx_gap:i+dx_gap+dx, jlow] = "_"
        ydata[i+dx_gap + (dx-1)/2, jhigh+1:jlow+1] = ":"

    print("\nTemp (C)")
    for i in range(ny+1):
        print yaxis[i], "".join(ydata.T[i])

    xaxisline = ("".join([" " for j in range(6)]) +
                 "".join(["_" for j in range(delta*nx)]))

    xaxislabel = "        " + "  ".join(xaxis)

    print(xaxisline)
    print(xaxislabel)
    print("".join((6+nx) * ["  "]) + xlabel)
    print("\n")


def get_ascii_icon(icon):
    if icon == "rain":
        ascii_icon =  [[r"/" if (i+j)%2 == 1 else " " for i in range(5)] for j in range(3)]
    elif icon == "wind":
        ascii_icon =  [[r"~" if (i+j)%2 == 0 else " " for i in range(5)] for j in range(3)]
    elif icon == "partly-cloudy-day":
        ascii_icon = [[" ", " ", "_", " ", " "],
                      [" ", "(", "_", ")", " "],
                      ["(", "_", "_", ")", ")"]]
    else:
        ascii_icon =  [[r" " for i in range(5)] for j in range(3)]

    return ascii_icon


def print_weather(icons, rows=3):
    ascii_icons = [get_ascii_icon(ic) for ic in icons]

    for row in range(rows):
        line = "        "
        for ic in ascii_icons:
            line += "".join(ic[row])
            line += "  "
        print line


def print_forecast(user_input_location, api_key):
    geolocator = Nominatim()
    location = geolocator.geocode(user_input_location, timeout=10)

    forecast = forecastio.load_forecast(api_key,
                                        location.latitude,
                                        location.longitude)

    current_temp = forecast.currently()

    print("Current temp is: {} Celcius".format(current_temp.temperature))
    try:
        print("Currently it is: {}".format(current_temp.summary))
    except forecastio.utils.PropertyUnavailable:
        pass
    try:
        print("Nearest storm is: {} miles".format(current_temp.nearestStormDistance))
    except forecastio.utils.PropertyUnavailable:
        pass


    byDay = forecast.daily()
    date = []
    lows = []
    highs = []
    icons = []
    for dailyData in byDay.data:
        date.append(dailyData.time)
        lows.append(dailyData.temperatureMin)
        highs.append(dailyData.temperatureMax)
        icons.append(dailyData.icon)

    xaxis = [date_formatter(d) for d in date]
    print_weather(icons)
    print_table(xaxis, lows, highs)


def InstallAPIKey(api_key_path):
    """ Attempts methods to help install the API key for user """

    if os.path.isfile(api_key_path):
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
            shutil.copyfile(local_src, api_key_path)
        except IOError:
            raise ValueError(
                "Failed to copy the local_src {} to {}".format(
                    local_src, api_key_path)
                )
    else:
        print("No file 'api.txt' found, attempt to get the information from\n"
              "the user.")
        api_string = raw_input(
            "\nIn order to use pyweather, you need a forecast.io api key. \n"
            "Please visit www.developer.forecast.io to register, and paste\n"
            "your API key below:\n\n")
        InstallAPIKeyFromString(api_key_path, api_string)


def InstallAPIKeyFromString(api_key_path, api_string):
        if api_string.isalnum() and len(api_string) == 32:
            print("\n Installing with API key '{}'".format(api_string))
            with open(api_key_path, "w+") as f:
                f.write(api_string)
        else:
            raise ValueError(
                "It appears the API key you have provided is of an invalid "
                "format")

def main():

    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--location", default=None, type=str,
                        help="Location for forecast", nargs='*')
    parser.add_argument("-a", "--print_api", action='store_true',
                        help="If called, print the current api key")
    parser.add_argument("-u", "--update_api", help="Update the api_key",
                        type=str)

    args = parser.parse_args()

    # Read in the api_key
    api_key_path = os.environ['HOME'] + '/.forecastio_apikey.txt'
    try:
        api_string = open(api_key_path, 'r').readline().rstrip("\n")
    except IOError:
        InstallAPIKey(api_key_path)
        return

    if args.print_api:
        print("Current api_key, stored in {} is: {}".format(
            api_key_path, api_string))
        return

    if args.update_api:
        InstallAPIKeyFromString(api_key_path, args.update_api)
        return

    if args.location:
        user_input_location = args.location
    else:
        user_input_location = raw_input("Enter your location: ")

    print_forecast(user_input_location, api_string)

if __name__ == "__main__":
    main()
