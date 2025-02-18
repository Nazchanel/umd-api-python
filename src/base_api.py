import requests

class BaseAPI:
    BASE_URL = 'https://api.umd.io/v1'

    def make_request(self, endpoint, **kwargs):
        # Automatically create params dictionary from method arguments
        params = self._extract_params(**kwargs)

        try:
            response = requests.get(f'{self.BASE_URL}/{endpoint}', params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.HTTPError as http_err:
            # Call handle_error if an HTTP error occurred
            self.handle_error(http_err, response)
        except requests.RequestException as err:
            print(f"An error occurred: {err}")
        except ValueError:
            print("Error: Received a non-JSON response.")

    def _extract_params(self, **kwargs):
        # Filter out None values from kwargs
        return {k: v for k, v in kwargs.items() if v is not None}

    def handle_error(self, http_err, response):
        """Handle HTTP error responses."""
        try:
            error_info = response.json()
            error_code = error_info.get("error_code", "Unknown error")
            message = error_info.get("message", "No message provided")
            docs = error_info.get("docs", "No documentation available")

            print(f"HTTP Error Code: {error_code}")
            print(f"Message: {message}")
            print(f"Documentation: {docs}")
        except ValueError:
            print(f"Received an error response, but couldn't parse JSON: {response.text}")
