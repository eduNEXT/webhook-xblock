"""
User module definitions for Open edX Sumac release.
"""
from openedx.core.djangoapps.user_api.accounts.serializers import AccountUserSerializer


def get_account_user_serializer():
    """
    Get AccountUserSerializer.

    Returns:
        AccountUserSerializer: AccountUserSerializer object.
    """
    return AccountUserSerializer
