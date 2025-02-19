import requests

class _BaseAPI:
    
    _BASE_URL = 'https://planetterp.com/api/v1'

    def _make_request(self, endpoint, **kwargs):
        params = self._extract_params(**kwargs)

        try:
            response = requests.get(f'{self._BASE_URL}/{endpoint}', params=params)
            response.raise_for_status() 
            return response.json()
        except requests.HTTPError as http_err:
            self._handle_error(http_err, response)
        except requests.RequestException as err:
            print(f"An error occurred: {err}")
        except ValueError:
            print("Error: Received a non-JSON response.")

    def _extract_params(self, **kwargs):
        return {k: v for k, v in kwargs.items() if v is not None}

    def _handle_error(self, http_err, response):
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
    
    def _bool_to_string(self, i):
        if type(i) != bool:
            raise ValueError("Must enter a boolean value")
        return "true" if i else "false"
