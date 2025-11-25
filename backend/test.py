import fastf1

fastf1.Cache.enable_cache("cache")

# Load weather data for the 2022 British Grand Prix race
race = fastf1.get_session(2022, 'British Grand Prix', 'Race')
race.load(weather=True)
weather = race.weather_data

print(weather['TrackTemp'])
print(weather['AirTemp'])
print(weather['Humidity'])
print(weather['Rainfall'])