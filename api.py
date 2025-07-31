from fastapi import FastAPI
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
API_KEY = "58a80029124e2e01724f48e80c7be2c0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Your existing weather endpoint
@app.get("/weather")
async def weather(city: str):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description']
        }
    return {"error": "City not found"}

# New route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: requests):
    return templates.TemplateResponse("index.html", {"request": request})