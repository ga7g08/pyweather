import forecastio
import re
from geopy.geocoders import Nominatim

geolocator = Nominatim()

api_key = open('api.txt', 'r').readline().rstrip("\n")

user_input_location = raw_input("Enter your location: ")

location = geolocator.geocode(user_input_location)

forecast = forecastio.load_forecast(api_key, location.latitude, location.longitude)

current_temp = forecast.currently()

print "Current temp is:",current_temp.temperature
print "Currently it is:",current_temp.summary
print "Nearest storm is:",current_temp.nearestStormDistance,"miles."


byDay = forecast.daily()
for dailyData in byDay.data:
   print dailyData.time,dailyData.temperatureMax,dailyData.temperatureMin

