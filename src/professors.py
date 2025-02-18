from src.base_api import BaseAPI  # Adjust import based on your structure

class Professors(BaseAPI):

    def list_professors(self, **kwargs):
        """
        
        Returns list of all professors
        
        """
        return self.make_request('professors', **kwargs)
