"""
User module generalized definitions.
"""
from importlib import import_module

from django.conf import settings


def get_serialized_user_account(*args, **kwargs):
    """Returns a serialized user account object."""
    backend = settings.WEBHOOK_USER_MODULE_BACKEND
    module = import_module(backend)
    return module.get_serialized_user_account(*args, **kwargs)
