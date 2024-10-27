"""Decorators."""

from __future__ import annotations

from functools import wraps


def singleton(cls) :
    """Create and maintain a single instance of an object.

    :param cls: The class to apply the singleton pattern to.
    :return: A decorated class instance that ensures only one instance of the class is created.
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
