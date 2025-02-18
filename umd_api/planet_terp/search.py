from .base_api import _BaseAPI

class Search(_BaseAPI):
    _ENDPOINT_SEARCH = 'search'

    def search(self, query, limit=None, offset=None):

        """

        Search both professors and courses with a query string. This will match professors and courses which have the query string as a substring of their name.
    
        """

        self._make_request(endpoint='search', query=query, limit=limit, offset=offset)
        