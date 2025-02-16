
from openmeteopy import OpenMeteo
from openmeteopy.options import DwdOptions
from openmeteopy.hourly import HourlyDwd
from openmeteopy.daily import DailyDwd
#from openmeteopy.fifteen_minutes import FiftennMinutesDwd
from PIL import ImageDraw
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import fonts
import datetime
import config

DARMSTADT_LAT_LON = [49.872826, 8.651193]
PADDING = 10
MIN_MAX_PLOT_FILENAME = "min_max_plot.jpg"

class Weather():

    def __init__(self):
        pass

    def draw(self, img: Image.Image, dryRun: bool):

        data = any
        if not dryRun:
            data = self._update()
        else:
            data = self._generate()

        width, height = img.size
        draw = ImageDraw.Draw(img)

        daily_data = data[1]
        hourly_data = data[0]

        # convert index date string into name of weekday
        daily_data['timetamp'] = daily_data.index
        daily_data['timetamp'] = pd.to_datetime(daily_data['timetamp'], format="%Y-%m-%d")
        daily_data['weekday'] = daily_data['timetamp'].dt.strftime('%A')
        daily_data['short_weekday'] = daily_data['timetamp'].dt.strftime('%a')
        
        print(daily_data)

        curr_temp = "{:02d}".format(round(hourly_data['temperature_2m'][0]))
        curr_wind_direction = "{:02d}".format(round(hourly_data['winddirection_10m'][0]))
        curr_wind_speed = "{:02d}".format(round(hourly_data['windspeed_10m'][0]))
        weather_code = hourly_data['weathercode'][0]
        max_temp = "{:02d}".format(round(daily_data['temperature_2m_max'][0]))
        min_temp = "{:02d}".format(round(daily_data['temperature_2m_min'][0]))
        print(f"temp max: {max_temp}, temp min: {min_temp}, weather code: {weather_code}")
        
        # current temp
        draw.text((width - 120, PADDING), curr_temp, (0,0,0), font=fonts.ROBO_NORM_120, anchor="rt")
        draw.text((width - 120, PADDING), fonts.weatherIcons['celsius'], (0,0,0), font=fonts.WEATHER_ICON_50, anchor="lt")

        # current weather code icon
        draw.text((int(width/2), PADDING), fonts.weatherCodeToIcon(weather_code), (0,0,0), font=fonts.WEATHER_ICON_70, anchor="mt")
                  
        # temperature min max
        draw.text((width-PADDING, PADDING), max_temp, (255,0,0) if daily_data['temperature_2m_max'][0] > 30 else (0,0,0), font=fonts.ROBO_LIGHT_50, anchor="rt")
        draw.text((width-PADDING, PADDING+50), min_temp, (0,0,255) if daily_data['temperature_2m_min'][0] < 5 else (0,0,0), font=fonts.ROBO_LIGHT_50, anchor="rt")

        # sunset and sunrise
        sunrise_time = datetime.datetime.strptime(daily_data['sunrise'][0], "%Y-%m-%dT%H:%M")
        sunset_time = datetime.datetime.strptime(daily_data['sunset'][0], "%Y-%m-%dT%H:%M")
        sunset_x = int(width/2)+45
        sunset_y = PADDING+240
        draw.text((sunset_x, sunset_y), fonts.weatherIcons['sunrise'], (0,0,0), font=fonts.WEATHER_ICON_25, anchor="mm")
        draw.text((sunset_x+60, sunset_y), sunrise_time.strftime("%H:%M"), (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="mm")
        draw.text((sunset_x, sunset_y+50), fonts.weatherIcons['sunset'], (0,0,0), font=fonts.WEATHER_ICON_25, anchor="mm")
        draw.text((sunset_x+60, sunset_y+50), sunset_time.strftime("%H:%M"), (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="mm")
        
        #draw.text((width-PADDING-80, PADDING+130), fonts.weatherIcons['sunrise'], (0,0,0), font=fonts.WEATHER_ICON_25, anchor="rm")
        #draw.text((width-PADDING, PADDING+130), sunrise_time.strftime("%H:%M"), (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="rm")
        #draw.text((width-PADDING-80, PADDING+170), fonts.weatherIcons['sunset'], (0,0,0), font=fonts.WEATHER_ICON_25, anchor="rm")
        #draw.text((width-PADDING, PADDING+170), sunset_time.strftime("%H:%M"), (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="rm")
        
        # wind direction and speed
        draw.text((width-PADDING, PADDING+240), curr_wind_speed + 'km/h', (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="rm")
        draw.text((width-PADDING, PADDING+290), curr_wind_direction + "°", (0,0,0), font=fonts.ROBO_LIGHT_30, anchor="rm")
        
        # weather icon forecast
        #forecast_x = int(width/2)+30
        #forecast_y = PADDING+130
        forecast_x = int(width/2)+45
        forecast_y = PADDING+120
        for idx in range(0, 5):
            draw.text((forecast_x, forecast_y), daily_data['short_weekday'][idx], (0,0,0),font=fonts.ROBO_LIGHT_30, anchor="mt")
            draw.text((forecast_x, forecast_y+30), fonts.weatherCodeToIcon(daily_data['weathercode'][idx]), (0,0,0), font=fonts.WEATHER_ICON_25, anchor="mt")    
            forecast_x += 70

        #for idx in range(0, len(daily_data.index)):
        #    draw.text((forecast_x, forecast_y), fonts.weatherCodeToIcon(daily_data['weathercode'][idx]), (0,0,0), font=fonts.WEATHER_ICON_25, anchor="lm")
        #    draw.text((forecast_x+50, forecast_y), daily_data['weekday'][idx], (0,0,0),font=fonts.ROBO_LIGHT_30, anchor="lm")
        #    forecast_y += 40
        
        # temperatur min max plot
        self._createMinMaxPlot(daily_data)
        plot_img = Image.open(MIN_MAX_PLOT_FILENAME)
        plot_width, plot_height = plot_img.size
        plot_ratio = plot_width / plot_height
        new_width = int(plot_ratio * height/1.6)
        plot_img = plot_img.resize((new_width, int(height/1.6)))
        img.paste(plot_img, ((PADDING,110)))

        
    def _createMinMaxPlot(self, data: pd.Series):

        plt.rc('xtick', labelsize=13)
        plt.rc('ytick', labelsize=13)

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.set_title("Temperatur (C°)", loc='left')
        ax1.plot(data['weekday'], data['temperature_2m_max'], linewidth=5)
        ax1.plot(data['weekday'], data['temperature_2m_min'], linewidth=5)
        ax1.tick_params(labelbottom = False)
        ax1.set_ylabel("Temp (C°)")
        ax1.yaxis.grid()

        ax2.set_title("Niederschlag (mm)", loc='left')
        ax2.plot(data['weekday'], data['precipitation_sum'], linewidth=5)
        ax2.tick_params(axis='x', rotation=15)
        ax2.set_ylabel("mm")
        ax2.yaxis.grid()

        fig.savefig(MIN_MAX_PLOT_FILENAME)
        
        
        #fig.savefig(MIN_MAX_PLOT_FILENAME)
#        plot = data.plot(x='weekday', rot=15, fontsize=13,  color=["red", "blue", "yellow"],  lw=5, label=["Maximum (C°)", "Minimum (C°)"], y=["temperature_2m_max", "temperature_2m_min"])
#        plot.set_xlabel("Tag")
#        plot.set_ylabel("Temperatur (°C)")
#        plot.grid(axis='y')
#        self.min_max_plot = plot.get_figure()
#        self.min_max_plot.savefig(MIN_MAX_PLOT_FILENAME)

    def _update(self) -> pd.DataFrame:
        hourly = HourlyDwd()
        daily = DailyDwd()
        options = DwdOptions(config.settings['weatherdisplay']['lat'],config.settings['weatherdisplay']['lon'])
        mgr = OpenMeteo(options, hourly.all(), daily.all())
        return mgr.get_pandas()

    def _generate(self):
        print("generating random weather data ...")
        pass        