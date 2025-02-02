"""
Grade module generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def get_student_course_grade(user, course_key):
    """Returns the CourseGrade for the given user in a specific course."""
    backend = settings.WEBHOOK_GRADE_MODULE_BACKEND
    module = import_module(backend)
    return module.get_course_grade_factory(user, course_key)
