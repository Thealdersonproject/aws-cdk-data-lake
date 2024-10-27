"""Utils for general usage purpose."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    """:param key: The name of the environment variable to retrieve.

    :return: The value of the environment variable if it is set, otherwise the default value.
    """
    return os.getenv(key, "")
