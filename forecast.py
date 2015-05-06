import forecastio
from geopy.geocoders import Nominatim
import numpy as np


def find_nearest(array,value):
    " Find the idx of nearest to value in array "
    idx = (np.abs(array-value)).argmin()
    return idx


def date_formatter(date):
    " Formats the x axis labels "
    return "{:02}/{:02}".format(date.month, date.day)


def print_table(xaxis, ylow, yhigh, ny=20, xlabel="Month/Year"):
    " Print ASCII table for range y1-> y2 "

    nx = len(highs)

    MAX = np.ceil(np.max(yhigh))
    MIN = np.floor(np.min(ylow))
    range_vals = np.linspace(MAX, MIN, ny+1)

    high_binned = [find_nearest(range_vals, val) for val in highs]
    low_binned = [find_nearest(range_vals, val) for val in lows]

    yaxis = ["{:04.01f} |".format(v) if i%2 == 0 else "     |"
             for (i, v) in enumerate(range_vals)]

    dx = 3 # Should be odd
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


geolocator = Nominatim()

api_key = open('api.txt', 'r').readline().rstrip("\n")

user_input_location = raw_input("Enter your location: ")

location = geolocator.geocode(user_input_location)

forecast = forecastio.load_forecast(api_key,
                                    location.latitude,
                                    location.longitude)

current_temp = forecast.currently()

print("Current temp is: {} Celcius".format(current_temp.temperature))
print("Currently it is: {}".format(current_temp.summary))
print("Nearest storm is: {} miles".format(current_temp.nearestStormDistance))

byDay = forecast.daily()
date = []
lows = []
highs = []
for dailyData in byDay.data:
    date.append(dailyData.time)
    lows.append(dailyData.temperatureMin)
    highs.append(dailyData.temperatureMax)

xaxis = [date_formatter(d) for d in date]
print_table(xaxis, lows, highs)
