"""
Grade module definitions for Open edX Sumac release.
"""
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory  # pylint: disable=import-error


def get_course_grade_factory():
    """
    Get CourseGradeFactory.

    Returns:
        CourseGradeFactory: CourseGradeFactory object.
    """
    return CourseGradeFactory
