import requests
import json
from bs4 import BeautifulSoup
import re
from pathlib import Path
from time import time
from datetime import  datetime

class Weather():
    def get_weather_data(self, station="", start_time="", end_time="", data=None): 
        
        """
        Valid Parameters:
        station: 'williams', 'atlantic', 'vmh', 'golf', 'chem'
        start_time and end_time must be in the following format: 'MM/DD/YY'
        Must be a valid range with end_time being after start_time.

        data is a list of the data points you want to fetch
        ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"] is default

        - If neither start_time nor end_time are provided → gets latest data only.
        - If start_time is provided but not end_time → gets data from start_time to present.
        - If end_time is provided but no start_time → raises ValueError.

        """

        DEFAULT_DATA_COLUMNS = ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"]
        
        if data is None:
            data = DEFAULT_DATA_COLUMNS

        invalid_columns = [item for item in data if item not in DEFAULT_DATA_COLUMNS]
        if invalid_columns:
            raise ValueError(f"Invalid values: {', '.join(invalid_columns)} are not in the predefined list.")
        
        current_data_flag = not start_time and not end_time
        
        url = "https://weather.umd.edu/wordpress/wp-content/plugins/meso-fsct/functions/get-data.php"
        
        stations_db = {
            "": "mesoterp7DB",
            "atlantic": "mesoterp7DB",
            "golf": "mesoterp6DB",
            "vmh": "mesoterp1DB",
            "williams": "mesoterp8DB",
            "chem": "mesoterp3DB"
        }
        
        if station.lower() not in stations_db:
            raise ValueError("Valid Station not Provided")
        
        def to_timestamp(date_str):
            return int(datetime.strptime(date_str, '%m/%d/%y').replace(hour=0, minute=0, second=0).timestamp())
        
        if end_time and not start_time:
            raise ValueError("Start Time Must be Provided")
        
        start_time = to_timestamp(start_time) if start_time else int(time()) - 120
        end_time = to_timestamp(end_time) if end_time else int(time())
        
        if end_time <= start_time:
            raise ValueError("End time must be greater than Start time")
        
        payload = {
            "startms": start_time, 
            "endms": end_time,
            "db": stations_db[station.lower()],
            "table": "archive",
            "cols": ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"]
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json().get("data")
            
            if not data:
                raise ValueError("No data returned from the API")
            
            if current_data_flag:
                return [{k: float(v) if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit() else v for k, v in data[0].items()}][0]
            else:
                return [{k: float(v) if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit() else v for k, v in row.items()} for row in data]
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    
    def save_radar_gif(self, dir=""):
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

    def get_weather_description(self):
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

    def get_co2_levels(self, start_time, end_time=None):

        """
        
        Fetch CO2 levels from the API.
        
        - `start_time` (str) must be provided in 'MM/DD/YY' format.
        - `end_time` (str, optional) defaults to the current time if not provided.
        - Start and end times must be at least one day apart.

        """
        
        url = "https://weather.umd.edu/wordpress/wp-content/plugins/meso-fsct/functions/get-data.php"
        
        def validate_date(date_str):
            try:
                return datetime.strptime(date_str, '%m/%d/%y')
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}. Expected format: MM/DD/YY")
        
        start_dt = validate_date(start_time)
        end_dt = validate_date(end_time) if end_time else datetime.utcnow()
        
        start_ts, end_ts = int(start_dt.timestamp()), int(end_dt.timestamp())
        
        if end_ts <= start_ts:
            raise ValueError("End time must be greater than Start time")
        
        if (end_ts - start_ts) < 86400:
            raise ValueError("Start to End range must be at least one day")
        
        payload = {
            "start_timestamp": start_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "end_timestamp": end_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "db": "atl_co2", # Only the Atlantic Building Station Provides Green House Gas Level
            "table": "co2_readings",
            "cols": ["timestamp", "measurement_value"]
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json().get('data', [])
            
            if not data:
                raise ValueError("No data returned from the API")
            
            for record in data:
                for key in record:
                    try:
                        record[key] = float(record[key])
                    except (ValueError, TypeError):
                        pass
            
            return data
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")
