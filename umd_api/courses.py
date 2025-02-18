from .base_api import _BaseAPI

class Courses(BaseAPI):
    
    _ENDPOINT_COURSES = 'courses'
    _ENDPOINT_MINIFIED_COURSES = 'courses/list'
    _ENDPOINT_SECTIONS = 'courses/sections'
    _ENDPOINT_SEMESTERS = 'courses/semesters'
    _ENDPOINT_DEPARTMENTS = 'courses/departments'

    def list_courses(self, sort=None, page=None, per_page=None, semester=None, credits=None, dept_id=None, gen_ed=None):

        """

        List all courses with optional filters.
        
        """
        return self.make_request(self._ENDPOINT_COURSES, sort, page, per_page, semester, credits, dept_id, gen_ed)

    def list_minified_courses(self, sort=None, page=None, per_page=None, semester=None):

        """

        List of minified courses (course codes and names).

        """
        
        return self.make_request(self._ENDPOINT_COURSES, sort, page, per_page, semester)

    def list_sections(self, sort=None, page=None, per_page=None, course_id=None, seats=None, open_seats=None, waitlist=None, semester=None):

        """
        
        List sections with optional filters.
        
        """
        
        return self.make_request(self._ENDPOINT_SECTIONS, sort, page, per_page, course_id, seats, open_seats, waitlist, semester)

    def view_specific_sections(self, section_ids, semester=None):
        
        """
        
        View specific sections by section IDs.
        
        """
        
        return self.make_request(f'{self._ENDPOINT_SECTIONS}/{section_ids}', semester)

    def view_specific_courses(self, course_ids, semester=None):
        
        """
        
        View specific courses by course IDs.
        
        """
        
        return self.make_request(f'{self._ENDPOINT_COURSES}/{course_ids}', semester)
        
    def view_sections_for_course(self, course_ids, semester=None):
        
        """
        
        View sections for specific courses.
        
        """
        
        return self.make_request(f'{self._ENDPOINT_COURSES}/{course_ids}/sections', semester)

    def view_specific_sections_for_course(self, course_ids, section_ids):
        
        """
        
        View specific sections for specific courses.
        
        """
        
        return self.make_request(f'{self._ENDPOINT_COURSES}/{course_ids}/sections/{section_ids}')

    def list_semesters(self):
        
        """
        
        List all available semesters.
        
        """
        
        return self.make_request(self._ENDPOINT_SEMESTERS)

    def list_departments(self):
        
        """
        
        List all available departments.
        
        """
        
        return self.make_request(self._ENDPOINT_DEPARTMENTS)
