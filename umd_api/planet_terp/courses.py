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

        if department is not None and len(department) != 4:
            raise ValueError("If provided, department must be exactly 4 characters long.")
    
        if limit is not None and not (1 <= limit <= 1000):
            raise ValueError("Limit must be between 1 and 1000 inclusive.")

        if offset is not None and offset < 0:
            raise ValueError("Offset must be a non-negative integer.")    
        
        return self._make_request(self._ENDPOINT_COURSES, department=department, reviews=self._bool_to_string(reviews), limit=limit, offset=offset)
