from src.courses import Courses

class UmdCoursesAPI:
    def __init__(self):
        self.courses = Courses()

if __name__ == '__main__':
    api = UmdCoursesAPI()
    try:
        # Example: List all minified courses
        minified_courses = api.courses.list_minified_courses(sort='course_id,-credits', per_page=10)
        for course in minified_courses:
            print(course)

        # Example: List sections for a specific course
        sections = api.courses.view_sections_for_course(course_ids='CMSC131')
        for section in sections:
            print(section)

        # Example: List all semesters
        semesters = api.courses.list_semesters()
        print(semesters)

        # Example: List all departments
        departments = api.courses.list_departments()
        print(departments)

    except Exception as e:
        print(f"An error occurred: {e}")
