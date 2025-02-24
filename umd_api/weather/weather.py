import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
from time import time
from datetime import datetime
import pytz
import os
import pandas as pd

class Weather:
    DEFAULT_DATA_COLUMNS = ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"]
    STATIONS_DB = {
        "": "mesoterp7DB",
        "atlantic": "mesoterp7DB",
        "golf": "mesoterp6DB",
        "vmh": "mesoterp1DB",
        "williams": "mesoterp8DB",
        "chem": "mesoterp3DB"
    }
    RADAR_URL = "https://weather.umd.edu/wordpress/wp-content/uploads/umdwx-temp/radar.gif"
    DATA_URL = "https://weather.umd.edu/wordpress/wp-content/plugins/meso-fsct/functions/get-data.php"

    def download_data(self, stations, output_format, output_dir="", start_time="", end_time="", data=None):
        if not isinstance(stations, list):
            raise ValueError("Stations Must be a List of Strings") 
    
        data = data or self.DEFAULT_DATA_COLUMNS

        # print(data)

        output_format = output_format.lower()

        if output_format not in ['xlsx', 'csv']:
            raise ValueError("Enter either csv or xlsx file format")
        
        output = {}
        for station in stations:
            output[station] = self.get_weather_data(station=station, start_time=start_time, end_time=end_time, data=data)
        
        # Change this line
        if output_format.lower() == 'xlsx':
            self._save_excel(output, output_dir)
            
        else:
            self._save_csv(output, output_dir)

    def get_weather_data(self, station="", start_time="", end_time="", data=None):
        """
        Fetch weather data for a specified station and time range.
        
        Valid Parameters:
        station: 'williams', 'atlantic', 'vmh', 'golf', 'chem'
        start_time and end_time must be in 'MM/DD/YY' format.
        If no time range is provided, gets the latest data.
        """
        data = data or self.DEFAULT_DATA_COLUMNS
        self._validate_data_columns(data)
        self._validate_station(station)
        
        start_time = self._convert_to_timestamp(start_time) if start_time else int(time()) - 120
        end_time = self._convert_to_timestamp(end_time) if end_time else int(time())
        
        if end_time <= start_time:
            raise ValueError("End time must be greater than Start time")
        
        payload = {
            "startms": start_time,
            "endms": end_time,
            "db": self.STATIONS_DB[station.lower()],
            "table": "archive",
            "cols": data
        }

        return self._fetch_data(payload)

    def save_radar_gif(self, dir=""):
        """
        Downloads the latest radar GIF and saves it to the specified directory.
        
        Args:
            dir (str): The directory where the GIF should be saved.
        
        Returns:
            str: The full path of the saved GIF.
        """
        save_path = Path(dir).expanduser().resolve()
        save_path.mkdir(parents=True, exist_ok=True)

        gif_file = save_path / "radar.gif"

        try:
            self._download_file(self.RADAR_URL, gif_file)
            print(f"Radar GIF saved successfully: {gif_file}")
            return str(gif_file)
        except Exception as e:
            print(f"Error saving radar GIF: {e}")

    def get_weather_description(self):
        """
        Fetch the current weather description from the website.
        
        Returns:
            str: Current weather description.
        """
        url = 'https://weather.umd.edu/'
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        weather_div = soup.find('div', class_='wxc_wx wxc_val')

        if weather_div:
            return weather_div.text.strip()
        else:
            raise ValueError("Weather condition not found in the HTML.")

    def get_co2_levels(self, start_time, end_time=None):
        """
        Fetch CO2 levels from the API.
        
        Args:
            start_time (str): Start date in 'MM/DD/YY' format.
            end_time (str, optional): End date in 'MM/DD/YY' format. Defaults to now if not provided.
        
        Returns:
            list: CO2 measurement records.
        """
        start_dt = self._validate_and_parse_date(start_time)
        end_dt = self._validate_and_parse_date(end_time) if end_time else datetime.utcnow()

        if (end_dt - start_dt).days < 1:
            raise ValueError("Start to End range must be at least one day")

        payload = {
            "start_timestamp": start_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "end_timestamp": end_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "db": "atl_co2",
            "table": "co2_readings",
            "cols": ["timestamp", "measurement_value"]
        }

        return self._fetch_co2_data(payload)

    def _fetch_data(self, payload):
        """Fetches weather data from the API."""
        try:
            response = requests.post(self.DATA_URL, json=payload)
            response.raise_for_status()
            data = response.json().get("data")

            if not data:
                raise ValueError("No data returned from the API")

            # Process all data without using current_data_flag
            return [self._process_row(row) for row in data]

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")


    def _fetch_co2_data(self, payload):
        """Fetches CO2 data from the API."""
        try:
            response = requests.post(self.DATA_URL, json=payload)
            response.raise_for_status()
            data = response.json().get('data', [])

            if not data:
                raise ValueError("No data returned from the API")

            for record in data:
                for key in record:
                    record[key] = self._convert_to_float(record[key])

            return data

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def _process_row(self, row):
        """Processes a single row of data."""
        return {k: self._convert_to_float(v) for k, v in row.items()}


    def _download_file(self, url, file_path):
        """Downloads a file from a URL and saves it to the specified path."""
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise for bad responses

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def _validate_data_columns(self, data):
        """Validates the data columns against the default list."""
        invalid_columns = [item for item in data if item not in self.DEFAULT_DATA_COLUMNS]
        if invalid_columns:
            raise ValueError(f"Invalid values: {', '.join(invalid_columns)} are not in the predefined list.")

    def _validate_station(self, station):
        """Validates the provided station against the known stations."""
        if station.lower() not in self.STATIONS_DB:
            raise ValueError("Valid Station not Provided")

    def _validate_and_parse_date(self, date_str):
        """Validates and parses a date string in 'MM/DD/YY' format."""
        try:
            return datetime.strptime(date_str, '%m/%d/%y')
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected format: MM/DD/YY")

    def _convert_to_timestamp(self, date_str):
        """Converts a date string in 'MM/DD/YY' format to a timestamp."""
        return int(datetime.strptime(date_str, '%m/%d/%y').replace(hour=0, minute=0, second=0).timestamp())

    def _convert_to_float(self, value):
        """Attempts to convert a value to a float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return value
    def _save_excel(self, data, dir=""):
        est_tz = pytz.timezone('America/New_York')
        save_path = Path(dir).expanduser().resolve()
        save_path.mkdir(parents=True, exist_ok=True)

        # Define a unique path for the Excel file to avoid overwriting
        excel_file = save_path / f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        try:
            # Create a Pandas Excel writer using Openpyxl as the engine
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                for station, records in data.items():
                    # Convert dateTime to EST and format it
                    for record in records:
                        # Check if dateTime is in string format, parse accordingly
                        if isinstance(record['dateTime'], str):
                            # If it's a string, you might want to parse it here based on the expected format
                            local_dt = datetime.fromisoformat(record['dateTime']).astimezone(pytz.utc)
                        else:
                            # Convert timestamp to a datetime object (assuming it's in seconds)
                            local_dt = datetime.fromtimestamp(record['dateTime'], tz=pytz.utc)

                        # Convert to EST
                        est_dt = local_dt.astimezone(est_tz)
                        # Format as a string
                        record['dateTime'] = est_dt.strftime('%Y-%m-%d %H:%M:%S')

                    # Create a DataFrame for each station
                    df = pd.DataFrame(records)
                    
                    # Write the DataFrame to a different sheet named after the station
                    df.to_excel(writer, sheet_name=station, index=False)

            print("Excel file created successfully at:", excel_file)

        except Exception as e:
            print("An error occurred while saving the Excel file:", e)
            
    def _save_csv(self, data, dir=""):
        # Define the output directory using Path
        output_directory = Path(dir) / 'weather_data_csv'
        output_directory.mkdir(parents=True, exist_ok=True)

        for station, records in data.items():
            df = pd.DataFrame(records)
            csv_filename = output_directory / f'{station}.csv'

            df.to_csv(csv_filename, index=False)
            print(f"Saved {csv_filename}")

        print("All CSV files created successfully.")

