"""
Grade module generalized definitions.
"""
from django.conf import settings

from webhook_xblock.edxapp_wrapper.base import BaseBackend


class GradeBackend(BaseBackend):
    """Wrapper for Grade module backend functions."""

    def __init__(self):
        """
        Cache the imported backend module to avoid repeated imports.
        """
        super().__init__(settings.WEBHOOK_GRADE_MODULE_BACKEND)

    def get_course_grade_factory(self):
        """Get CourseGradeFactory object."""
        return self.backend.get_course_grade_factory()


user_backend = GradeBackend()

get_course_grade_factory = user_backend.get_course_grade_factory
