"""
Utils functions for the XBlock.
"""
from collections.abc import MutableMapping


def flatten_dict(d, parent_key='', sep='_'):
    """
    This function returns a flatten dictionary-like object.
    """
    items = []
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)
