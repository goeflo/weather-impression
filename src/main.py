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


