from .base_api import _BaseAPI

class Courses(_BaseAPI):
    _ENDPOINT_COURSE = 'course'
    _ENDPOINT_COURSES = 'courses'

    def get_course(self, name, reviews=None):

        """

        Gets the specified courses

        """

        return self._make_request(self._ENDPOINT_COURSE, name=name, reviews=reviews)

    def get_courses(self, department=None, reviews=None, limit=None, offset=None):
        
        """

        Get all courses, in alphabetical order

        """
        
        return self._make_request(self._ENDPOINT_COURSES, department=department, reviews=reviews, limit=limit, offset=offset)
