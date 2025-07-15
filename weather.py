import requests

# Get your API key from OpenWeatherMap
API_KEY = "58a80029124e2e01724f48e80c7be2c0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    # Build the API request URL
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        print(f"🌤️ Weather in {city}: {temp}°C, {description}")
    else:
        print("❌ Error fetching data. Check city name or API key.")

# Get user input
city_name = input("Enter a city: ")
get_weather(city_name)
