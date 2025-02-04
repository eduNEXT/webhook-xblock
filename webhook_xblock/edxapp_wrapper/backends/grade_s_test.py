"""
Grades module test definitions for Open edX Sumac release.
"""


def get_student_course_grade(user, course_key):
    """
    Returns an object to avoid import error when executing
    unit tests.

    Returns:
        object if import fails.
    """
    try:
        from lms.djangoapps.grades.course_grade_factory import \
            CourseGradeFactory  # pylint: disable=import-outside-toplevel
    except ImportError:
        CourseGradeFactory = object
    return CourseGradeFactory().read(user, course_key=course_key)
