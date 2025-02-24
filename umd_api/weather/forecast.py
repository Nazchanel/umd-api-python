import requests
import re
from bs4 import BeautifulSoup

class Forecast:
    BASE_URL = "https://weather.umd.edu/"

    def get_hourly_forecast(self):
        """Fetches the hourly weather forecast for the next five hours."""
        hourly_forecast = []
        soup = self._fetch_soup()

        forecast_div = soup.find('div', id="umdwx_weeklyfcst_widget-9")
        if not forecast_div:
            raise ValueError("Hourly forecast data not found on the page.")

        for day in forecast_div.find_all('div', class_='fcst_day')[:5]:
            forecast = self._parse_hourly_forecast(day)
            if forecast:
                hourly_forecast.append(forecast)

        return hourly_forecast

    def get_weekly_forecast(self):
        """Fetches the weekly weather forecast."""
        weekly_forecast = []
        soup = self._fetch_soup()

        forecast_div = soup.find('div', id="umdwx_weeklyfcst_widget-9")
        if not forecast_div:
            raise ValueError("Weekly forecast data not found on the page.")

        for day in forecast_div.find_all('div', class_='fcst_day')[5:]:
            forecast = self._parse_weekly_forecast(day)
            if forecast:
                weekly_forecast.append(forecast)

        return weekly_forecast

    def _fetch_soup(self):
        """Fetches the HTML content and returns a BeautifulSoup object."""
        response = requests.get(self.BASE_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return BeautifulSoup(response.text, 'html.parser')

    def _parse_hourly_forecast(self, day):
        """Parses the hourly forecast data from a single day element."""
        time = day.find('div', class_='fcst_txt-day').text.strip()
        temp_div = day.find('div', class_='fcst_txt-temp')
        wind_div = day.find('div', class_='fcst_txt-wind')

        if temp_div and wind_div:
            temp = self._clean_temperature(temp_div.text)
            wind = self._clean_wind_speed(wind_div.text)

            hour, period = self._convert_time_to_24_hour_format(time)
            return {'time': hour, 'temperature': temp, 'wind': wind}

        return None

    def _parse_weekly_forecast(self, day):
        """Parses the weekly forecast data from a single day element."""
        day_name_div = day.find('div', class_='fcst_txt-day')
        temp_range_div = day.find('div', class_='fcst_txt-temp')

        if day_name_div and temp_range_div:
            day_name = self._fix_day_name(day_name_div.text)
            high_temp, low_temp = self._extract_temperatures(temp_range_div.text)
            return {'day': day_name, 'high': high_temp, 'low': low_temp}

        return None

    def _clean_temperature(self, temp_text):
        """Cleans and formats the temperature text."""
        return temp_text.replace('\u2009', ' ').replace('F', '').strip()

    def _clean_wind_speed(self, wind_text):
        """Cleans and formats the wind speed text."""
        return re.sub(r'[^\x00-\x7F]+', '', wind_text).replace('mph', '').strip()

    def _convert_time_to_24_hour_format(self, time_text):
        """Converts the 12-hour format time to 24-hour format."""
        hour, period = time_text.split()
        hour = int(hour)

        if period == 'PM' and hour != 12:
            hour += 12
        elif period == 'AM' and hour == 12:
            hour = 0

        return hour, period

    def _fix_day_name(self, day_name):
        """Fixes specific typos in day names."""
        return 'Thu' if day_name == 'Thi' else day_name

    def _extract_temperatures(self, temp_range_text):
        """Extracts high and low temperatures from the temperature range text."""
        temp_values = temp_range_text.split(' / ')
        if len(temp_values) == 2:
            high_temp = self._clean_temperature(temp_values[0])
            low_temp = self._clean_temperature(temp_values[1])
            return high_temp, low_temp
        return None, None
