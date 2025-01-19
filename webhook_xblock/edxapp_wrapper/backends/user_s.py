"""
User module definitions for Open edX Sumac release.
"""
from django.contrib.auth import get_user_model
from openedx.core.djangoapps.user_api.accounts.serializers import AccountUserSerializer


def get_edx_user_model():
    """
    Get current Open edX User model.
    """
    return get_user_model()


def get_account_user_serializer():
    """
    Get AccountUserSerializer.

    Returns:
        AccountUserSerializer: AccountUserSerializer object.
    """
    return AccountUserSerializer
