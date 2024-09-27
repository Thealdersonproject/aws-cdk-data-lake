# resource name pattern separator
DEFAULT_RESOURCE_NAME_PATTERN_SEPARATOR: str = "-"
HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR: str = "-"
UNDERSCORE_RESOURCE_NAME_PATTERN_SEPARATOR: str = "_"
SLASH_RESOURCE_NAME_PATTERN_SEPARATOR: str = "/"
BACK_SLASH_RESOURCE_NAME_PATTERN_SEPARATOR: str = "\\"

"""
    ::: aws general name pattern :::
"""
DEFAULT_RESOURCE_NAME_PATTERN: str = \
    "account-environment#<resource_short_name>#<resource_name>"
    # "{environment}{separator}{company_short_name}{separator}{project_short_name}{separator}{resource_short_name}{separator}{resource_logical_name}"


DEFAULT_ENCODING = "UTF-8"
