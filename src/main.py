#!/usr/bin/env python3
# display size 800 x 480

import os
import argparse
import weather
import time
import datetime
import fonts
import config
from PIL import Image
from PIL import ImageDraw
from inky.auto import auto

PATH = os.path.dirname(__file__)
PADDING = 10

def main():

    
    parser = argparse.ArgumentParser()
    parser.add_argument("--export", "-e", action="store_false", required=False, help="export image to jpg file, do not refresh inky display")
    parser.add_argument("--dryRun", "-d", action="store_true", required=False, help="dry run, do not request external data sources")
    args, _ = parser.parse_known_args()

    export = args.export
    dryRun = args.dryRun

    print('inky, refresh display:{}, dry run: {}, update interval:{} Minutes'.format(export, dryRun, config.settings['weatherdisplay']['updateInterval']))

    w = weather.Weather()
    dt = DateTime()

    while True:
    
        img = Image.new("RGB", (800,480), color='white')
        dt.draw(img)
        w.draw(img, dryRun)

        if not export:
            img.save(os.path.join(PATH, "display.jpg"))
            os._exit(os.EX_OK)

        updateInkyDisplay(img, dryRun)
        
        time.sleep(60 * config.settings['weatherdisplay']['updateInterval'])

#------------------------------------------------------------------------------
class DateTime():
    def __init__(self):
        pass

    def draw(self, img) -> Image.Image:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        now = datetime.datetime.now()
        day_of_week = now.strftime("%A")        
        day_of_month = now.strftime("%d")
        month = now.strftime("%B")
        timestamp = now.strftime("%X")

        draw.text((PADDING, PADDING), day_of_week, (0,0,0), font=fonts.RORO_NORM_60, anchor="lt")
        draw.text((PADDING, 80), day_of_month + " " + month, (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="lt")

        # timestamp
        draw.text((PADDING, height-PADDING), "update time: " + timestamp, (100,100,100), font=fonts.ROBO_LIGHT_20, anchor="lb")


#def generateImage(img, meteo):
#        draw = ImageDraw.Draw(img)
#        width, height = img.size
#
#        roboNorm60 = fonts.getFont(fonts.Type.ROBO_NORM, 60)
#        roboLight120 = fonts.getFont(fonts.Type.ROBO_LIGHT, 120)
#        roboLight20 = fonts.getFont(fonts.Type.ROBO_LIGHT, 20)
#        roboLight30 = fonts.getFont(fonts.Type.ROBO_LIGHT, 30)
#        roboLight50 = fonts.getFont(fonts.Type.ROBO_LIGHT, 50)
#        weatherIcon50 = fonts.getFont(fonts.Type.WEATHER_ICON, 50)
#        weatherIcon100 = fonts.getFont(fonts.Type.WEATHER_ICON, 70)
#
#        #locale.setlocale(locale.LC_TIME, 'de_DE')
#        now = datetime.datetime.now()
#        dayOfWeek = now.strftime("%A")        
#        dayOfMonth = now.strftime("%d")
#        month = now.strftime("%B")
#        timestamp = now.strftime("%X")
#
#        # day of week
#        dayOfWeekWidth, dayOfWeekHeight = fonts.getWidthHeight(roboNorm60, dayOfWeek)
#        draw.text((PADDING, PADDING), dayOfWeek, (0,0,0), font=roboNorm60, anchor="lt")
#
#        currentTemperature = "{:02d}".format(round(meteo.current_temp))
#        maxTemperature = "{:02d}".format(round(meteo.day_max_temp))
#        minTemperature = "{:02d}".format(round(meteo.day_min_temp))
#
#        tempWidth, tempHeight = fonts.getWidthHeight(roboLight120, currentTemperature)
#
#        # day of month
#        dayOfMonthWidth, dayOfMonthHeight = fonts.getWidthHeight(roboLight30, dayOfMonth)
#        draw.text((PADDING, PADDING+tempHeight-dayOfMonthHeight), dayOfMonth, (0,0,0), font=roboLight30, anchor="ls")
#
#        # month
#        draw.text((dayOfMonthWidth+PADDING*2, PADDING+tempHeight-dayOfMonthHeight), month, (0,0,0), font=roboLight30, anchor="ls")
#
#        # temperature
#        draw.text((width - tempWidth, PADDING), currentTemperature, (0,0,0), font=roboLight120, anchor="rt")
#        celsiusWidth, celsiusHeight = fonts.getWidthHeight(weatherIcon50, fonts.weatherIcons['celsius'])
#        draw.text((width - tempWidth + celsiusWidth, PADDING), fonts.weatherIcons['celsius'], (0,0,0), font=weatherIcon50, anchor="rt")
#
#        # temperature max
#        draw.text((width-PADDING, PADDING), maxTemperature, (255,0,0) if meteo.day_max_temp > 30 else (0,0,0), font=roboLight50, anchor="rt")
#
#        # temperature min
#        tempMinWidth, tempMinHeigt = fonts.getWidthHeight(roboLight50, minTemperature)
#        draw.text((width-PADDING, PADDING*3+tempHeight-tempMinHeigt), minTemperature, (0,0,255) if meteo.day_min_temp < 5 else (0,0,0), font=roboLight50, anchor="rb")
#
#        # waether icon
#        draw.text((width / 2 , PADDING), fonts.weatherCodeToIcon(meteo.weather_code, meteo.is_day), (0,0,0), font=weatherIcon100, anchor="mt")
#        
#        # timestamp
#        _, tHeight = fonts.getWidthHeight(roboLight20, timestamp)
#        draw.text((0, height-tHeight), "update time: " + timestamp, (100,100,100), font=roboLight20, anchor="lt")
#
#        # temperatur min max plot
#        plot_img = Image.open(os.path.join(PATH, "min_max_temp.jpg"))
#        
#
#        plot_width, plot_height = plot_img.size
#        plot_ratio = plot_width / plot_height
#        new_width = int(plot_ratio * height/1.5)
#        plot_img = plot_img.resize((new_width, int(height/2)))
#        img.paste(plot_img, ((PADDING,110)))
#        
#
#        return img


def updateInkyDisplay(img, dryRun):
    if dryRun:
        return

    try:
        inky_display = auto(ask_user=True, verbose=True)
    except TypeError:
        raise TypeError("you need to update the inky library tp >= v1.1.0")

    # TODO scale image size

    inky_display.set_image(img)
    inky_display.show()


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()


