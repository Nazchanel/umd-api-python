from .base_api import _BaseAPI

class Courses(_BaseAPI):
    _ENDPOINT_COURSE = 'course'
    _ENDPOINT_COURSES = 'courses'

    def get_course(self, name, reviews=False):

        """

        Gets the specified courses

        """

        return self._make_request(self._ENDPOINT_COURSE, name=name, reviews=self._bool_to_string(reviews))

    def get_courses(self, department=None, reviews=False, limit=100, offset=0):

        """

        Get all courses, in alphabetical order

        """

        return self._make_request(self._ENDPOINT_COURSES, department=department, reviews=self._bool_to_string(reviews), limit=limit, offset=offset)
