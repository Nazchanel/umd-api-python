from .base_api import _BaseAPI

class Professors(_BaseAPI):
    _ENDPOINT_PROFESSOR = 'professor'
    _ENDPOINT_PROFESSORS = 'professors'

    def get_professor(self, name: str, reviews=False):

        """

        Get the specified professor.

        """

        return self._make_request(self._ENDPOINT_PROFESSOR, name=name, reviews=self._bool_to_string(reviews))

    def get_all_professors(self, type=None, reviews=False, limit=100, offset=0):

        """

        Get all professors, in alphabetical order

        """

        return self._make_request(self._ENDPOINT_PROFESSORS, type=type, reviews=self._bool_to_string(reviews), limit=limit, offset=offset)
