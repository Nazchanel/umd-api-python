from src.base_api import BaseAPI

class Courses(BaseAPI):
    ENDPOINT_COURSES = 'courses'
    ENDPOINT_MINIFIED_COURSES = 'courses/list'
    ENDPOINT_SECTIONS = 'courses/sections'
    ENDPOINT_SEMESTERS = 'courses/semesters'
    ENDPOINT_DEPARTMENTS = 'courses/departments'

    def list_courses(self, **kwargs):
        """
        List all courses with optional filters.
        """
        return self.make_request(self.ENDPOINT_COURSES, **kwargs)

    def list_minified_courses(self, **kwargs):
        """
        List of minified courses (course codes and names).
        """
        return self.make_request(self.ENDPOINT_MINIFIED_COURSES, **kwargs)

    def list_sections(self, **kwargs):
        """
        List sections with optional filters.
        """
        return self.make_request(self.ENDPOINT_SECTIONS, **kwargs)

    def view_specific_sections(self, section_ids, **kwargs):
        """
        View specific sections by section IDs.
        """
        return self.make_request(f'{self.ENDPOINT_SECTIONS}/{section_ids}', **kwargs)

    def view_specific_courses(self, course_ids, **kwargs):
        """
        View specific courses by course IDs.
        """
        return self.make_request(f'{self.ENDPOINT_COURSES}/{course_ids}', **kwargs)

    def view_sections_for_course(self, course_ids, **kwargs):
        """
        View sections for specific courses.
        """
        return self.make_request(f'{self.ENDPOINT_COURSES}/{course_ids}/sections', **kwargs)

    def view_specific_sections_for_course(self, course_ids, section_ids, **kwargs):
        """
        View specific sections for specific courses.
        """
        return self.make_request(f'{self.ENDPOINT_COURSES}/{course_ids}/sections/{section_ids}', **kwargs)

    def list_semesters(self):
        """
        List all available semesters.
        """
        return self.make_request(self.ENDPOINT_SEMESTERS)

    def list_departments(self):
        """
        List all available departments.
        """
        return self.make_request(self.ENDPOINT_DEPARTMENTS)
