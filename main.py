from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

# Define a Tool class that inherits from BaseTool
class Tool(BaseTool):
    def __init__(self, name, description, func):
        super().__init__(name=name, description=description)
        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _run(self, *args, **kwargs):
        return self.run(*args, **kwargs)

import requests

# Replace with your actual OpenWeatherMap API key
OPENWEATHER_API_KEY = "your_api_key_here"

# Tool: Geocoding function
def get_coordinates(city):
    try:
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json"}
        )
        data = response.json()
        if not data:
            return None
        return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
    except Exception as e:
        print(f"Error in geocoding: {e}")
        return None

# Tool: Weather fetching function
def get_weather(coords):
    try:
        lat, lon = coords["lat"], coords["lon"]
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        )
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None
# Wrap functions as CrewAI tools
geocode_tool = Tool(
    name="Geocode City",
    description="Get the latitude and longitude for a given city.",
    func=get_coordinates
)
weather_tool = Tool(
    name="Fetch Weather",
    description="Fetch the current weather for given coordinates.",
    func=get_weather
)

# Define agents
geocoder = Agent(
    role="Geocoder",
    goal="Get the latitude and longitude for a given city.",
    backstory="Expert in geocoding and location services.",
    tools=[geocode_tool]
)
weather_fetcher = Agent(
    role="WeatherFetcher",
    goal="Fetch the current weather for given coordinates.",
    backstory="Expert in weather data retrieval.",
    tools=[weather_tool]
)


# CLI interface
if __name__ == "__main__":
    city = input("Enter a city name: ")
    crew = Crew(agents=[geocoder, weather_fetcher])

    # Define tasks for each agent
    geocode_task = Task(
        agent=geocoder,
        description=f"Get the latitude and longitude for {city}.",
        expected_output="Coordinates of the city."
    )
    weather_task = Task(
        agent=weather_fetcher,
        description=f"Fetch the current weather for the coordinates provided by the geocoder.",
        expected_output="Current weather information."
    )

    # Assign tasks to the crew and execute them
    crew.tasks = [geocode_task, weather_task]
    results = ''
    print(results)
