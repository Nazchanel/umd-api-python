from .base_api import _BaseAPI

class Map(_BaseAPI):
    
    _ENDPOINT_BUILDINGS = 'map/buildings'
    
    def list_buildings(self):
        
        """

        Get a list of the available buildings.

        """

        return self._make_request(f'{self._ENDPOINT_BUILDINGS}')
    
    def get_buildings(self, building_id : list):
        
        """

        Get location data about one or more buildings. Comma separated building numbers are the parameters.

        """
        
        buildings_formatted = ','.join(building_id)

        return self._make_request(f'{self._ENDPOINT_BUILDINGS}/{buildings_formatted}')
    
