import requests
import json
from bs4 import BeautifulSoup
import re
from pathlib import Path
from time import time
from datetime import  datetime

class Weather():
    def get_weather_data(station="", start_time="", end_time=""): 
        """
        Valid Parameters:
        station: 'williams', 'atlantic', 'vmh', 'golf', 'chem'
        start_time and end_time must be in the following format: 'MM/DD/YY'
        Must be a valid range with end_time being after start_time.

        - If neither start_time nor end_time are provided → gets latest data only.
        - If start_time is provided but not end_time → gets data from start_time to present.
        - If end_time is provided but no start_time → raises ValueError.

        """

        url = "https://weather.umd.edu/wordpress/wp-content/plugins/meso-fsct/functions/get-data.php"

        station = station.lower()
        db = ""

        current_data_flag = False

        def validate_date_format(date_str):
            try:
                if date_str:  # Only validate if the string is not empty
                    datetime.strptime(date_str, '%m/%d/%y')
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}. Expected format: MM/DD/YY")

        # Ensure start_time is provided if end_time is set
        if start_time == '' and end_time != '':
            raise ValueError("Start Time Must be Provided")

        # Validate date formats if they are provided
        if start_time != '':
            validate_date_format(start_time)
        if end_time != '':
            validate_date_format(end_time)

        # Convert provided times to Unix timestamps
        if start_time != '' and end_time != '':
            start_time = int(datetime.strptime(start_time, '%m/%d/%y').replace(hour=0, minute=0, second=0).timestamp())
            end_time = int(datetime.strptime(end_time, '%m/%d/%y').replace(hour=0, minute=0, second=0).timestamp())
        elif start_time != '' and end_time == '':
            start_time = int(datetime.strptime(start_time, '%m/%d/%y').replace(hour=0, minute=0, second=0).timestamp())
            end_time = int(time())
        elif start_time == '' and end_time == '':
            current_data_flag = True

            start_time = int(time()) - 120  # 2 minutes ago
            end_time = int(time())  # Now

        if end_time <= start_time:
            raise ValueError("End time must be greater than Start time")

        match station:
            case '':
                db = 'mesoterp7DB'
            case 'atlantic':
                db = "mesoterp7DB"
            case 'golf':
                db = "mesoterp6DB"
            case 'vmh':
                db = "mesoterp1DB"
            case 'williams':
                db = "mesoterp8DB"
            case 'chem':
                db = "mesoterp3DB"
            case _:
                raise ValueError("Valid Station not Provided")


        PAYLOAD = {
            "startms": start_time,
            "endms": end_time,
            "db": db,
            "table": "archive",
            "cols": ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"]
        }

        try:
            result = requests.post(url, json=PAYLOAD)
            result.raise_for_status()  # Raise error for bad HTTP responses
            data = result.json().get('data')

            if not data:
                raise ValueError("No data returned from the API")

            result_dict = {}

            if current_data_flag:
                result_dict = data[0]

                for key in result_dict:
                    try:
                        result_dict[key] = float(result_dict[key])
                    except (ValueError, TypeError):
                        pass
            else:
                result_dict = data

                for i in range(len(result_dict)):
                    for key in result_dict[i]:
                        try:
                            result_dict[i][key] = float(result_dict[i][key])
                        except (ValueError, TypeError):
                            pass

            return result_dict

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
    
    def get_hourly_forecast():    
        hourly_forecast = []
        url = "https://weather.umd.edu/"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.find('div', id="umdwx_weeklyfcst_widget-9")

        for day in a.find_all('div', class_='fcst_day')[:5]:  # First 5 elements are hourly forecast
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

            
            if time and temp and wind:  # Ensure elements exist
                hourly_forecast.append({
                    'time': time,
                    'temperature': temp,
                    'wind': wind
                })
        return hourly_forecast


    def save_radar_gif(dir=""):
        """
        Downloads the latest radar GIF and saves it to the specified directory.
        
        Args:
            dir (str): The directory where the GIF should be saved. If no directory is specified, downloads to current directory.
        
        Returns:
            str: The full path of the saved GIF.
        """
        gif_url = "https://weather.umd.edu/wordpress/wp-content/uploads/umdwx-temp/radar.gif"
        
        # Convert to Path object for better handling
        save_path = Path(dir).expanduser().resolve()

        try:
            # Create directory if it doesn't exist
            save_path.mkdir(parents=True, exist_ok=True)

            # Define file path
            gif_file = save_path / "radar.gif"

            # Download the GIF
            response = requests.get(gif_url, stream=True)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

            # Write content to file
            with open(gif_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # Efficient chunk download
                    file.write(chunk)

            print(f"Radar GIF saved successfully: {gif_file}")
            return str(gif_file)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading radar GIF: {e}")
        except OSError as e:
            print(f"Error saving file: {e}")

    def get_weather_description():
        url = 'https://weather.umd.edu/'

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            weather_div = soup.find('div', class_='wxc_wx wxc_val')

            if weather_div:
                weather_text = weather_div.text.strip()
                return weather_text
            else:
                raise ValueError("Weather condition not found in the HTML.")
        else:
            raise requests.exceptions.HTTPError(f"Failed to fetch the webpage. Status code: {response.status_code}")

