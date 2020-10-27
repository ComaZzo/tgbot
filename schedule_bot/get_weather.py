import requests


def get_weather():
    api_key = 'b7c3bf30db57e2f7836f1894ae6fe079'
    url = f'http://api.openweathermap.org/data/2.5/weather?q=moscow&APPID={api_key}'
    json_weather = requests.get(url).json()
    degree_sign = u'\N{DEGREE SIGN}'
    response = f"The weather in Moscow today:\n"\
               f"{json_weather['weather'][0]['description']}\n"\
               f"Temperature: {round(json_weather['main']['temp'] - 273)} {degree_sign}С\n"\
               f"Feels like: {round(json_weather['main']['feels_like']- 273)} {degree_sign}С\n"\
               f"Minimal temperature: {round(json_weather['main']['temp_min']-273)} {degree_sign}С\n"\
               f"Humidity: {round(json_weather['main']['humidity'])}%"
    return response
