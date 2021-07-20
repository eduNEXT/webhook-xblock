"""
Utils functions for the XBlock.
"""
import collections


def flatten_dict(d, parent_key='', sep='_'):
    """
    This function returns a flatten dictionary-like object.
    """
    items = []
    for key, value in d.items():
        new_key = "{parent_key}{sep}{key}".format(parent_key=parent_key, sep=sep, key=key) if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)
