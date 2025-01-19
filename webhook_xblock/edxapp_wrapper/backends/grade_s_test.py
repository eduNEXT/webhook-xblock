"""
Grades module test definitions for Open edX Sumac release.
"""


def get_course_grade_factory():
    """
    Return a fake CourseGradeFactory object to avoid import error when executing
    unit tests.

    Returns:
        object if import fails.
    """
    try:
        from lms.djangoapps.grades.course_grade_factory import \
            CourseGradeFactory  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseGradeFactory = object
    return CourseGradeFactory
