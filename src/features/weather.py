import requests

API_KEY = "b65d9260c453ef6f20ef3fe961bf7f22"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    if API_KEY == "PLACEHOLDER_KEY":
        return "Please configure the Open Weather Map API key in the weather module."

    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404" and data.get("main"):
            main_data = data["main"]
            temperature_kelvin = main_data["temp"]

            temperature_celsius = temperature_kelvin - 273.15
            weather_desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temperature_celsius:.1f} degrees Celsius with {weather_desc}."
        else:
            return "I could not find the weather for that city."
    except Exception as e:
        return "I could not fetch the weather data right now."

def process_weather(query):

    if "weather" in query or "wheter" in query or "wether" in query:
        words = query.split()
        for prep in ["in", "of", "at"]:
            if prep in words:
                idx = words.index(prep)
                if idx + 1 < len(words):
                    city = words[idx + 1]
                    return get_weather(city)

        if len(words) > 1 and words[-2] == "weather":
            return get_weather(words[-1])

        return "Please specify the city, for example, say 'weather in London' or 'weather of Jaipur'."
    return None
