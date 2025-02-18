from .base_api import _BaseAPI

class Bus(_BaseAPI):
    
    _ENDPOINT_ROUTES = 'bus/routes'
    _ENDPOINT_STOPS = 'bus/stops'

    def list_routes(self):

        """

        Get a list of the available routes.

        """

        return self._make_request(self._ENDPOINT_ROUTES)
    
    
    def view_specific_routes(self, route_ids : list):
        
        """

        Get route data for one or more routes

        """
        
        routes_formatted = ','.join(route_ids)
        
        return self._make_request(f'{self._ENDPOINT_ROUTES}/{routes_formatted}')
    
    
    def list_stops(self):

        """
        
        Get a list of the available stops.

        """

        return self._make_request(self._ENDPOINT_STOPS)

   
    def get_specific_stops(self, stop_ids : list):

        """

        Get data for one or more stops

        """

        # Formatting
        stop_ids_str = ""

        for i in stop_ids:
            stop_ids_str += "stop_id="
            stop_ids_str += i
            stop_ids_str += "&"

        return self._make_request(f'{self._ENDPOINT_STOPS}?{stop_ids_str}')

    def current_bus_locations_by_route(self, route_id):

        """

        Get bus locations for a route

        """

        return self._make_request(f'{self._ENDPOINT_ROUTES}/{route_id}/locations')

    def bus_schedules(self, route_id):

        """

        Get bus schedules for a route

        """

        return self._make_request(f'{self._ENDPOINT_ROUTES}/{route_id}/schedules')

    def get_arrivals_for_stop(self, route_id, stop_id):

        """
        
        Get arrivals for a stop for a route

        """

        return self._make_request(f'{self._ENDPOINT_ROUTES}/{route_id}/arrivals/{stop_id}')
