"""
User module definitions for Open edX Sumac release.
"""
from openedx.core.djangoapps.user_api.accounts.serializers import AccountUserSerializer  # pylint: disable=import-error


def get_serialized_user_account(*args, **kwargs):
    """
    Get a Serialized User Account.

    Returns:
       An  AccountUserSerializer instanced object
    """
    return AccountUserSerializer(*args, **kwargs)
