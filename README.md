# BaroMetric
Display variations of atmospheric pressure. 

The LaMetric app "Barometer (Atmo Pressure)" takes the pressure every 1 hour from OpenWeatherMap.org. Use the city name and country Iso2 code as parameters. If not found, Noumea, NC will be used. Script : PressureWebService.py. Set your static IP and port at the end of the script. The app has also to be setup with your public IP and public port.

The LaMetric app "AtmoPressure Geneva" update Geneva Switzerland pressure info every 2 hours. Script : AccessWebService.py  

Use nohup to start the scripts in the background.
