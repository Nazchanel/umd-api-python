from .base_api import _BaseAPI

class Professors(_BaseAPI):

    def list_professors(self, name=None, course_id=None):
        """
        
        Returns list of all professors
        
        """
        return self._make_request('professors', name, course_id)
