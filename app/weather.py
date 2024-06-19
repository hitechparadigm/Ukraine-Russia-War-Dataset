from datetime import datetime, timedelta
from pymeteosource.api import Meteosource
from pymeteosource.types import tiers, sections, langs, units

# Change this to your actual API key
YOUR_API_KEY = 'sxz7rlz4v623scbzl0y0btyv00kllqiw59lmplda'
# Change this to your actual tier
YOUR_TIER = tiers.FREE

# Initialize the main Meteosource object
meteosource = Meteosource(YOUR_API_KEY, YOUR_TIER)

# Get the forecast for given point
forecast = meteosource.get_point_forecast(
    lat=37.7775,  # Latitude of the point
    lon=-122.416389,  # Longitude of the point
    place_id=None,  # You can specify place_id instead of lat+lon
    sections=[sections.CURRENT, sections.HOURLY],  # Defaults to '("current", "hourly")'
    tz='US/Pacific',  # Defaults to 'UTC', regardless of the point location
    lang=langs.ENGLISH,  # Defaults to 'en'
    units=units.US  # Defaults to 'auto'
)

# Forecast for lat: 37.7775, lon: -122.416389
print(forecast)
