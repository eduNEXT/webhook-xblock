"""
User module generalized definitions.
"""
from webhook_xblock.edxapp_wrapper.base import BaseBackend
from django.conf import settings


class UserBackend(BaseBackend):
    """Wrapper for User module backend functions."""

    def __init__(self):
        """
        Cache the imported backend module to avoid repeated imports.
        """
        super().__init__(settings.WEBHOOK_USER_MODULE_BACKEND)

    def get_account_user_serializer(self):
        """Get AccountUserSerializer object."""
        return self.backend.get_account_user_serializer()


user_backend = UserBackend()

account_user_serializer = user_backend.get_account_user_serializer
