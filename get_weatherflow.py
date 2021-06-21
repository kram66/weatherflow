from urllib.request import urlopen
import json
from datetime import datetime
import pymongo

#Following are the JSON types, add your own!
#Sky (type="obs_sky")
#Observation Layout
#0 - Epoch (seconds UTC)
#1 - Illuminance (lux)
#2 - UV (index)
#3 - Rain Accumulation (mm)
#4 - Wind Lull (m/s)
#5 - Wind Avg (m/s)
#6 - Wind Gust (m/s)
#7 - Wind Direction (degrees)
#8 - Battery (volts)
#9 - Report Interval (minutes)
#10 - Solar Radiation (W/m^2)
#11 - Local Day Rain Accumulation (mm)
#12 - Precipitation Type (0 = none, 1 = rain, 2 = hail, 3 = rain + hail (experimental))
#13 - Wind Sample Interval (seconds)
#14 - Rain Accumulation Final (Rain Check) (mm)
#15 - Local Day Rain Accumulation Final (Rain Check) (mm)
#16 - Precipitation Analysis Type (0 = none, 1 = Rain Check with user display on, 2 = Rain Check with user display off)

token = "[put your token here]"
device_id = "[put your device id here]"

# Get the dataset
url = 'https://swd.weatherflow.com/swd/rest/observations/?device_id=' + device_id + '&token=' + token
response = urlopen(url)

# Convert bytes to string type and string type to dict
string = response.read().decode('utf-8')
json_obj = json.loads(string)

#setup the data we want to capture
Now = datetime.now()
Feels = json_obj['summary']['feels_like']
UV = json_obj['obs'][0][2]
Rain = json_obj['obs'][0][3]
Wind = json_obj['obs'][0][5]
WindDir = json_obj['obs'][0][7]
Radiation= json_obj['obs'][0][10]

mydict = {"date": str(Now), "Feels_Like": Feels, "UV Index": UV, "Rain": Rain, "Wind": Wind, "WindDir": WindDir, "Radiation": Radiation  }
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["weather"]
mycol = mydb["currentdata"]

x = mycol.insert_one(mydict)
