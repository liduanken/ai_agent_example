
from fastagent import FastAgent

agent = FastAgent(name="WeatherAgent", server="http://localhost:8000/sse")
agent.run()
