from urllib.request import urlopen
import json
from datetime import datetime
import pymongo
import datetime


def convertepoc(epoc):
	x = datetime.datetime.fromtimestamp(epoc).strftime('%d/%m/%Y %I:%M:%S %p')
	return x

def convertepocday(epoc):
	x = datetime.datetime.fromtimestamp(epoc).strftime('%A, %d-%m')
	return x
	
token = "[token here]"
station_id = "[your station id here]"
device_id = "[your device id here]"

# Get the rain dataset
rainurl = 'https://swd.weatherflow.com/swd/rest/observations/?device_id=' + device_id + '&token=' + token
response = urlopen(rainurl)
string = response.read().decode('utf-8')
json_obj = json.loads(string)
rain_lasthour = json_obj['summary']['precip_total_1h']
rain_yesterday = json_obj['summary']['precip_accum_local_yesterday']

# Get the dataset
url = "https://swd.weatherflow.com/swd/rest/better_forecast?station_id=" + station_id + "&units_temp=c&units_wind=kph&units_pressure=mb&units_precip=mm&units_distance=km&token=" + token
response = urlopen(url)

# Convert bytes to string type and string type to dict
string = response.read().decode('utf-8')
json_obj = json.loads(string)

#setup the data we want to capture
now = datetime.datetime.now()
Current = json_obj['current_conditions']['conditions']
TempNow = json_obj['current_conditions']['air_temperature']
UV = json_obj['current_conditions']['uv']
Humidity = json_obj['current_conditions']['relative_humidity']
wind_average  = json_obj['current_conditions']['wind_avg']
wind_direction = json_obj['current_conditions']['wind_direction']
wind_direction_cardinal = json_obj['current_conditions']['wind_direction_cardinal']
wind_gust = json_obj['current_conditions']['wind_gust']
solar_radiation  = json_obj['current_conditions']['solar_radiation']
brightness = json_obj['current_conditions']['brightness']
feels_like  = json_obj['current_conditions']['feels_like']
dew_point  = json_obj['current_conditions']['dew_point']

#Since we can calculate this on location, no need to write this
Sunrise  = json_obj['forecast']['daily'][1]['sunrise']
Sunset  = json_obj['forecast']['daily'][1]['sunset']

#Define some Json to insert into our Mongo DB"
mydict = {"date": str(now), "Current": Current, "TempNow": TempNow, "Feels_Like": feels_like, "UV Index": UV, "Humidity": Humidity, "WindAverage": wind_average, "WindDirection": wind_direction, "WindCardina": wind_direction_cardinal, "WindGust": wind_gust, "SolarRadiation": solar_radiation, "Brightness": brightness, "Rain": rain_lasthour, "Rain_Yesterday": rain_yesterday}

#Connect and write the record
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["weather"]
mycol = mydb["currentdata"]
x = mycol.insert_one(mydict)

#Lets print out the next forcast to the console
for key in json_obj['forecast']['daily']:
	#print(key)
	print('Day:', convertepocday(key['day_start_local']), 'Conditions:', key['conditions'], 'High:', key['air_temp_high'], 'Low:', key['air_temp_low'], 'Sunrise:', convertepoc(key['sunrise']), 'Sunset:', convertepoc(key['sunset']))

