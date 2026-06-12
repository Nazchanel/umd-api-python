import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from datetime import datetime
import pytz
import pandas as pd

class Weather:
    DEFAULT_DATA_COLUMNS = ["dateTime", "outTemp", "dewpoint", "barometer", "rainRate", "windSpeed", "windGust", "windDir"]
    STATIONS_DB = {
        "": "mesoterp13DB",
        "atlantic": "mesoterp13DB",
        "williams": "mesoterp8DB",
        "chem": "mesoterp3DB",
        "chesapeake": "mesoterp10DB",
        "esicc": "mesoterp12DB",
        "golf": "mesoterp6DB",
        "observatory": "mesoterp2DB",
        "van_munching":"mesoterp1DB",
        "technology_ventures": "mesoterp11DB"
    }
    
    RADAR_URLS = {
        "image_loop":"https://radar.weather.gov/ridge/standard/KLWX_loop.gif",
        "latest_image":"https://radar.weather.gov/ridge/standard/KLWX_0.gif"
        }
    
    DATA_URL = "https://weather.umd.edu/wordpress/wp-content/plugins/meso-fsct/functions/get-data.php"

    def download_data(self, stations, output_format, output_dir="", start_time="", end_time="", data=None):
        if not isinstance(stations, list):
            raise ValueError("Stations Must be a List of Strings") 
    
        data = data or self.DEFAULT_DATA_COLUMNS

        output_format = output_format.lower()

        if output_format not in ['xlsx', 'csv']:
            raise ValueError("Enter either csv or xlsx file format")
        
        output = {}
        for station in stations:
            output[station] = self.get_weather_data(station=station, start_time=start_time, end_time=end_time, data=data)
        
        if output_format.lower() == 'xlsx':
            self._save_excel(output, output_dir)
            
        else:
            self._save_csv(output, output_dir)

    from datetime import datetime
    import time

    def get_weather_data(self, station="", start_time="", end_time="", data=None):
        """
        Fetch weather data for a specified station and time range.

        Valid Parameters:
        station: 'williams', 'atlantic', 'vmh', 'golf', 'chem'
        start_time/end_time format: 'MM/DD/YY HH:MM AM/PM'
        If no time range is provided, gets the latest data.
        """
        data = data or self.DEFAULT_DATA_COLUMNS
        self._validate_data_columns(data)
        self._validate_station(station)

        def parse_time(t):
            # expects: "MM/DD/YY HH:MM AM/PM"
            return int(datetime.strptime(t, "%m/%d/%y %I:%M %p").timestamp())

        # defaults: last 2 minutes
        now = int(time.time())

        start_time = parse_time(start_time) if start_time else now - 120
        end_time = parse_time(end_time) if end_time else now

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

    def save_radar_gif(self, dir="", image_type="loop"):
        """
        Downloads the latest radar GIF and saves it to the specified directory.
        
        Args:
            dir (str): The directory where the GIF should be saved.
            image_type (str): Either "loop" or "latest", defaults to loop
        Returns:
            str: The full path of the saved GIF.
        """
  
        RADAR_URL = _validate_radar(image_type)
        
        save_path = Path(dir).expanduser().resolve()
        save_path.mkdir(parents=True, exist_ok=True)

        gif_file = save_path / "radar.gif"

        try:
            self._download_file(RADAR_URL, gif_file)
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
        url = 'https://weather.umd.edu/wordpress/micronet/'
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

    def _validate_radar(self, radar_opt):
        if radar_opt == "loop":
            return self.RADAR_URLS["image_loop"]
        elif radar_opt == "latest":
            return self.RADAR_URLS["latest_image"]
        else:
            raise ValueError(f"Invalid value: {radar_opt}.")

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
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                for station, records in data.items():
                    for record in records:
                        if isinstance(record['dateTime'], str):
                            local_dt = datetime.fromisoformat(record['dateTime']).astimezone(pytz.utc)
                        else:
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
        output_directory = Path(dir) / "weather_data_csv"
        output_directory.mkdir(parents=True, exist_ok=True)

        est_tz = pytz.timezone("America/New_York")

        for station, records in data.items():

            # convert timestamps → readable time
            for record in records:
                dt = datetime.fromtimestamp(record["dateTime"], tz=pytz.utc)
                record["dateTime"] = dt.astimezone(est_tz).strftime("%Y-%m-%d %I:%M:%S %p")

            df = pd.DataFrame(records)

            csv_filename = output_directory / f"{station}.csv"
            df.to_csv(csv_filename, index=False)

            print(f"Saved {csv_filename}")

        print("All CSV files created successfully.")
