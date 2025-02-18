from .base_api import _BaseAPI

class Majors(_BaseAPI):
    
    def list_majors(self):
        
        """

        Get a list of all majors

        """

        return self._make_request('majors/list')
