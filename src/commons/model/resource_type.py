# mypy: ignore-errors
from __future__ import annotations

from pydantic import BaseModel, Field


class ResourceType(BaseModel):
    """
    This module defines a class `ResourceType` that represents a resource type.

    Attributes:
        - `product_name`: The name of the product associated with the resource type. It is a string.
        - `short_name`: The short name of the resource type. It is a string with a maximum length of 3 characters.
        - `description`: An optional description of the resource type. It is a string or None.
        - `resource_group`: The resource group associated with the resource type. It is a string.
        - `resource_tags`: An optional dictionary of resource tags. It is a dictionary or None.
        - `name_pattern_separator`: The separator used in the name pattern of the resource type. It is a string with a length of 1.

    """

    product_name: str = Field(min_length=1)
    product_description: str | None = Field(default=None)
    product_web_link: str | None = Field(default=None)
    short_name: str = Field(min_length=1)
    resource_type: str = Field(min_length=1)
    resource_tags: dict = Field(default=None)
    name_pattern_separator: str = Field(min_length=1, max_length=1)
    name_pattern_regex: str | None = Field(default=None)
