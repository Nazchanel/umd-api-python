from src.base_api import BaseAPI

class Majors(BaseAPI):
    def list_majors(self):
        
        """

        Get a list of all majors

        """

        return self.make_request('majors/list')
