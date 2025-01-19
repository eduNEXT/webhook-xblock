"""
User module test definitions for Open edX Sumac release.
"""


def get_edx_user_model():
    """
    Return current Open edX custom User model.
    """
    try:
        from django.contrib.auth import get_user_model  # pylint: disable=import-outside-toplevel
        return get_user_model()
    except ImportError:
        from django.contrib.auth.models import User  # pylint: disable=import-outside-toplevel
        return User


def get_account_user_serializer():
    """
    Return a fake serializer to avoid import error when executing
    unit tests.

    Returns:
        object if import fails.
    """
    try:
        from openedx.core.djangoapps.user_api.accounts.serializers import \
            AccountUserSerializer  # pylint: disable=import-outside-toplevel
    except ImportError:
        AccountUserSerializer = object
    return AccountUserSerializer
