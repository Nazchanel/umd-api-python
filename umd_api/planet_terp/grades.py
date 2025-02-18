from .base_api import _BaseAPI

class Grades(_BaseAPI):
    _ENDPOINT_GRADES = "grades"

    def get_grades(self, course=None, professor=None, semester=None, section=None):

        """

        Get grades for a course, a professor, or both. If by course, returns all of the grades available by section.

        """

        return self._make_request(self._ENDPOINT_GRADES, course=course, professor=professor, semester=semester, section=section)

