
from crewai import Crew, Agent, Task
from tools.geocoding_tool import get_coordinates
from tools.weather_tool import get_weather

geocoder = Agent(name="Geocoder", function=get_coordinates)
weather_fetcher = Agent(name="WeatherFetcher", function=get_weather)

crew = Crew(agents=[geocoder, weather_fetcher])
crew.run("Get weather for London")
