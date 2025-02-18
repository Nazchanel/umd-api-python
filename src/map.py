from src.base_api import BaseAPI

class Map(BaseAPI):
    ENDPOINT_BUILDINGS = 'map/buildings'
    
    def list_buildings(self):
        
        """

        Get a list of the available buildings.

        """

        return self.make_request(f'{self.ENDPOINT_BUILDINGS}')
    
    def get_buildings(self, building_id):
        
        """

        Get location data about one or more buildings. Comma separated building numbers are the parameters.

        """
        
        return self.make_request(f'{self.ENDPOINT_BUILDINGS}/{building_id}')
    
