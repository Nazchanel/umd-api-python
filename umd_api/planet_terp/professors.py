from .base_api import _BaseAPI

class Professors(_BaseAPI):
    _ENDPOINT_PROFESSOR = 'professor'
    _ENDPOINT_PROFESSORS = 'professors'

    def get_professor(self, name, reviews=None):

        """

        Get the specified professor.

        """

        return self._make_request(self._ENDPOINT_PROFESSOR, name, reviews)
    
    def get_all_professors(self, type=None, reviews=None, limit=None, offset=None):
        
        """

        Get all professors, in alphabetical order

        """
        
        return self._make_request(self._ENDPOINT_PROFESSORS, type=type, reviews=reviews, limit=limit, offset=offset)
