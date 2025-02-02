"""
Grade module definitions for Open edX Sumac release.
"""
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory  # pylint: disable=import-error


def get_course_grade_factory(user, course_key):
    """
    Returns the CourseGrade for the given user in the course.

    Returns:
        A CourseData object.
    """
    return CourseGradeFactory().read(user, course_key=course_key)
