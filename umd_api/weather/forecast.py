import requests
import re
from bs4 import BeautifulSoup

class Forecast():

    def get_hourly_forecast(self):
        hourly_forecast = []
        url = "https://weather.umd.edu/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.find('div', id="umdwx_weeklyfcst_widget-9")

        for day in a.find_all('div', class_='fcst_day')[:5]:
            time = day.find('div', class_='fcst_txt-day').text.strip()
            temp = day.find('div', class_='fcst_txt-temp')
            wind = day.find('div', class_='fcst_txt-wind')
            
            temp =  temp.text.replace('\u2009', ' ').replace('F', ' ').strip()

            wind = re.sub(r'[^\x00-\x7F]+', '', wind.text)

            wind = wind.replace('mph', '').strip()
            
            hour, period = time.split()

            hour = int(hour)
            
            if period == 'PM' and hour != 12:
                hour += 12
            elif period == 'AM' and hour == 12:
                hour = 0

            time = hour

            
            if time and temp and wind:
                hourly_forecast.append({
                    'time': time,
                    'temperature': temp,
                    'wind': wind
                })
        return hourly_forecast

    def get_weekly_forecast(self):  
        url = "https://weather.umd.edu/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        a = soup.find('div', id="umdwx_weeklyfcst_widget-9")
    
        weekly_forecast = []
        weekly_forecast_start = 5  # Skip first part for weekly forecast
        for day in a.find_all('div', class_='fcst_day')[weekly_forecast_start:]:
            day_name = day.find('div', class_='fcst_txt-day')
            temp_range = day.find('div', class_='fcst_txt-temp')
            
            if day_name and temp_range:
                # Fix Thursday typo in website
                if day_name.text == 'Thi':
                    day_name = 'Thu'
                else:
                    day_name = day_name.text

                # Extract high and low temperatures
                temp_values = temp_range.text.split(' / ')  # Split by the separator
                if len(temp_values) == 2:  # Ensure we have both high and low values
                    high_temp = temp_values[0].replace('\u2009', ' ').strip()  # Remove narrow space
                    low_temp = temp_values[1].replace('\u2009', ' ').strip()  # Remove narrow space
                    high_temp = temp_values[0].replace('F', ' ').strip()
                    low_temp = temp_values[1].replace('F', ' ').strip()
                    weekly_forecast.append({
                        'day': day_name,
                        'high': high_temp,
                        'low': low_temp
                    })

        return weekly_forecast
