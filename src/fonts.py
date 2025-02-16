from enum import Enum
from PIL import ImageFont
import os

PATH = os.path.dirname(__file__)

class Type(Enum):
    ROBO_THIN = PATH + "/fonts/Roboto-Thin.ttf"
    ROBO_LIGHT =  PATH + "/fonts/Roboto-Light.ttf"
    ROBO_NORM = PATH + "/fonts/Roboto-Black.ttf"
    WEATHER_ICON = PATH + "/fonts/weathericons-regular-webfont.ttf"

def getFont(font, size):
    return ImageFont.truetype(font.value, size)

def getWidthHeight(font, text):
    _, _, width, height = font.getbbox(text)
    return (width, height)

RORO_NORM_60 = getFont(Type.ROBO_NORM, 60)
ROBO_NORM_120 = getFont(Type.ROBO_LIGHT, 120)
ROBO_LIGHT_20 = getFont(Type.ROBO_LIGHT, 20)
ROBO_LIGHT_30 = getFont(Type.ROBO_LIGHT, 30)
ROBO_LIGHT_50 = getFont(Type.ROBO_LIGHT, 50)
WEATHER_ICON_25 = getFont(Type.WEATHER_ICON, 25)
WEATHER_ICON_50 = getFont(Type.WEATHER_ICON, 50)
WEATHER_ICON_70 = getFont(Type.WEATHER_ICON, 70)

# https://open-meteo.com
MAINLY_CLEAR = [1, 2]
OVERCAST = [3]
FOG = [45,48]
DRIZZLE = [51, 53, 55]
FREEZING_DRIZZLE = [56, 57]
RAIN = [61, 63, 65]
FREEZING_RAIN = [66, 67]
SNOW = [71, 73, 75]
RAIN_SHOWER = [80, 81, 82]
SNOW_SHOWER = [85, 86]
THUNDERSTORM = [95, 96, 99]

def windDirectionToIcon(direction: int):
    pass

def weatherCodeToIcon(code: int):
    match code:
        case 0:
            return weatherIcons['alien']
        case code if code in MAINLY_CLEAR:
            return weatherIcons['day-sunny']
        case code if code in OVERCAST:
            return weatherIcons['day-sunny-overcast']
        case code if code in FOG:
            return weatherIcons['fog']
        case code if code in DRIZZLE:
            return weatherIcons['sprinkle']
        case code if code in FREEZING_DRIZZLE:
            return weatherIcons['sleet']
        case code if code in RAIN:
            return weatherIcons['rain']
        case code if code in FREEZING_RAIN:
            return weatherIcons['hail']
        case code if code in SNOW:
            return weatherIcons['snow']
        case code if code in RAIN_SHOWER:
            return weatherIcons['showers']
        case code if code in SNOW_SHOWER:
            return weatherIcons['snow']
        case code if code in THUNDERSTORM:
            return weatherIcons['thunderstorm']
        case _:
            return weatherIcons['alien']
    
weatherIcons = {
    'dir-up':'\uf058',
    'dir-up-right':'\uf057',
    'dir-right':'\uf04d',
    'dir-down-right':'\uf088',
    'dir-down':'\uf044',
    'dir-down-lef':'\uf043',
    'dir-left':'\uf048',
    'dir-up-left':'\uf087',

    'day-sunny':'\uf00d',
    'day-sunny-overcast':'\uf00c',
    'cloud':'\uf041',
    'cloudy':'\uf013',
    'cloudy-gust':'\uf011',
    'cloudy-windy':'\uf012',
    'fog':'\uf014',
    'hail':'\uf015',
    'rain':'\uf019',
    'rain-mix':'\uf017',
    'rain-wind':'\uf018',
    'showers':'\uf01a',
    'sleet':'\uf0b5',
    'snow':'\uf01b',
    'sprinkle':'\uf01c',
    'storm-showers':'\uf01d',
    'thunderstorm':'\uf01e',
    'snow-wind':'\uf064',
    'snow':'\uf01b',
    'lightning':'\uf016',

    'celsius':'\uf03c',
    'sunrise':'\uf051',
    'sunset':'\uf052',
    'alien':'\uf075'

}