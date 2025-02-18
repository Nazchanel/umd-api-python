from src.base_api import BaseAPI

class Bus(BaseAPI):
    ENDPOINT_ROUTES = 'bus/routes'
    ENDPOINT_STOPS = 'bus/stops'

    def list_routes(self, **kwargs):

        """

        Get a list of the available routes.

        """

        return self.make_request(self.ENDPOINT_ROUTES, **kwargs)
    
    
    def view_specific_routes(self, route_ids):
        
        """

        Get route data for one or more routes

        """

        return self.make_request(f'{self.ENDPOINT_ROUTES}/{route_ids}')
    
    
    def list_stops(self):

        """
        
        Get a list of the available stops.

        """

        return self.make_request(self.ENDPOINT_STOPS)

   
    def get_specific_stops(self, stop_ids):

        """

        Get data for one or more stops

        """

        return self.make_request(f'{self.ENDPOINT_STOPS}/{stop_ids}')

    def current_bus_locations_by_route(self, route_id):

        """

        Get bus locations for a route

        """

        return self.make_request(f'{self.ENDPOINT_ROUTES}/{route_id}/locations')

    def bus_schedules(self, route_id):

        """

        Get bus schedules for a route

        """

        return self.make_request(f'{self.ENDPOINT_ROUTES}/{route_id}/schedules')

    def get_arrivals_for_stop(self, route_id, stop_id):

        """
        
        Get arrivals for a stop for a route

        """

        return self.make_request(f'{self.ENDPOINT_ROUTES}/{route_id}/arrivals/{stop_id}')
