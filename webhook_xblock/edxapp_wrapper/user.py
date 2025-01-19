"""
User module generalized definitions.
"""
from django.conf import settings

from webhook_xblock.edxapp_wrapper.base import BaseBackend


class UserBackend(BaseBackend):
    """Wrapper for User module backend functions."""

    def __init__(self):
        """
        Cache the imported backend module to avoid repeated imports.
        """
        super().__init__(settings.WEBHOOK_USER_MODULE_BACKEND)

    def get_edx_user_model(self):
        """Get Open edX custom User model."""
        return self.backend.get_edx_user_model()

    def get_account_user_serializer(self):
        """Get AccountUserSerializer object."""
        return self.backend.get_account_user_serializer()


user_backend = UserBackend()

edx_user_model = user_backend.get_edx_user_model
account_user_serializer = user_backend.get_account_user_serializer
