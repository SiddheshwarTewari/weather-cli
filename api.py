from fastapi import FastAPI
import requests

app = FastAPI()
API_KEY = "58a80029124e2e01724f48e80c7be2c0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.get("/weather")
def get_weather(city: str):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description']
        }
    else:
        return {"error": "City not found"}

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)