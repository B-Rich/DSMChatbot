from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json


def present():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=daejeon,kr&units=metric'
    service_key = '709f54e9062fdbadbe73863ff0ac30b5'

    queryParams = '&' + urlencode({quote_plus('APPID'): service_key})
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = (urlopen(request).read()).decode("utf-8")
    WeatherData = json.loads(response_body)

    # 파싱을 실행하는 부분입니다. JSON 변환 후 리스트 슬라이싱을 사용했습니다
    weather = WeatherData['weather'][0]
    weather = weather['description']
    temp_min = WeatherData['main']['temp_min']
    temp_max = WeatherData['main']['temp_max']

    humidity = WeatherData['main']['humidity']
    temp = WeatherData['main']['temp']
    present_weather = [weather, temp, temp_max, temp_min, humidity]

    return present_weather

def week():
    url = "http://api.openweathermap.org/data/2.5/forecast?q=daejeon,kr&units=metric"
    service_key = '709f54e9062fdbadbe73863ff0ac30b5'

    queryParams = '&' + urlencode({quote_plus('APPID'): service_key})
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = (urlopen(request).read()).decode("utf-8")
    WeatherData = json.loads(response_body)
    day1 = WeatherData["list"][5]
    day2 = WeatherData["list"][12]
    day3 = WeatherData["list"][19]
    day4 = WeatherData["list"][26]
    day5 = WeatherData['list'][34]

    day1 = [day1['main']['temp'], day1['weather'][0]["description"]]
    day2 = [day2['main']['temp'], day2['weather'][0]["description"]]
    day3 = [day3['main']['temp'], day3['weather'][0]["description"]]
    day4 = [day4['main']['temp'], day4['weather'][0]["description"]]
    day5 = [day5['main']['temp'], day5['weather'][0]["description"]]

    days = [day1, day2, day3, day4, day5]

    return days

def air_cond():
    url = "http://apis.skplanetx.com/weather/dust"

    queryParams = '?' + urlencode({quote_plus('lon'): 127.363409}) + '&' + urlencode({quote_plus('lat') : 36.391465}) + '&' + urlencode({quote_plus('version') : 1})
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = (urlopen(request).read()).decode("utf-8")
    WeatherData = json.loads(response_body)

    return WeatherData
