from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
API_KEY = "58a80029124e2e01724f48e80c7be2c0"
BASE_URL = "https://api.openweathermap.org/data/2.5"

templates = Jinja2Templates(directory="templates")

@app.get("/weather")
async def weather(city: str, units: str = "metric"):
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data['name'],
            "country": data['sys']['country'] if 'country' in data['sys'] else '',
            "temperature": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "unit": units,
            "coord": data['coord']  # Add coordinates for the map
        }
    return {"error": "City not found"}

@app.get("/forecast")
async def forecast(city: str, units: str = "metric"):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        daily_forecasts = []
        # Group by day (8 forecasts per day, every 3 hours)
        for i in range(0, min(40, len(data['list'])), 8):
            day = data['list'][i]
            daily_forecasts.append({
                "date": day['dt_txt'].split()[0],
                "temp": day['main']['temp'],
                "feels_like": day['main']['feels_like'],
                "description": day['weather'][0]['description'],
                "icon": day['weather'][0]['icon'],
                "humidity": day['main']['humidity'],
                "wind_speed": day['wind']['speed']
            })
        return {
            "city": data['city']['name'],
            "country": data['city']['country'],
            "forecasts": daily_forecasts,
            "unit": units,
            "coord": data['city']['coord']  # Add coordinates for the map
        }
    return {"error": "City not found"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})