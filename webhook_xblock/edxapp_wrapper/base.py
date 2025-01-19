"""
Base class for generalized backend Open edX definitions.
"""

from importlib import import_module


class BaseBackend:
    """Base class for backend wrapper functions."""

    def __init__(self, backend_setting):
        """
        Initialize the backend by importing the module specified
        in the setting.

        Args:
            backend_setting (str): The Django setting specifying the
            backend module path.
        """
        self.backend = import_module(backend_setting)
