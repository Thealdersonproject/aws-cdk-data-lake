# mypy: ignore-errors
from __future__ import annotations

import re
from typing import Dict

from pydantic import BaseModel, Field

from commons.utils import constants
from commons.utils.loader import Loader


class Resource(BaseModel):
    """
    Resource class representing various resources with a structured naming pattern.

    Attributes:
        resource_type (ResourceType): The type of the resource.
        logical_name (str): The logical name of the resource.
        resource_name_pattern (str): The pattern used to generate the resource name.
        resource_name_pattern_separator (str): The separator used in the resource name pattern.

    Properties:
        resource_name (str): Generates a resource name based on the provided pattern and various attributes.
        tags (Dict[str, str]): A dictionary of tags associated with the resource.

    Methods:
        load_resource(logical_name: str, resource_type: ResourceType): Loads and returns a Resource object with the given logical name and resource type.
    """

    logical_name: str
    resource_description: str
    product_name: str = Field(min_length=1)
    product_description: str | None = Field(default=None)
    product_web_link: str | None = Field(default=None)
    short_name: str = Field(min_length=1)
    resource_type: str | None = Field(min_length=1)
    resource_name_pattern: str
    resource_name_pattern_replace_map: Dict[str, str]
    resource_name_pattern_separator: str = Field(min_length=1, max_length=1)
    resource_name_pattern_regex: str | None = Field(default=None)

    # pylint: disable=all
    @property
    def resource_name(self) -> str:
        """
            resource_name
            Generate a formatted resource name based on a pattern and various environmental variables.

            Returns:
                str: The generated resource name.
        """
        loader = Loader()
        value = self.resource_name_pattern.format(
            company_information_short_name=loader.company.short_name,
            environment_variables_environment=loader.account.environment,
            project_short_name=loader.project.short_name,
            resource_logical_name=self.logical_name,
            resource_short_name=self.short_name,
            separator=self.resource_name_pattern_separator,
        )
        value = value.strip()
        value = value.strip("-").strip()
        value = re.sub(r"-+", "-", value)
        value = re.sub(r"_+", "_", value)
        value = re.sub(r"\s+", " ", value)
        value = value.replace(" ", "_")
        value = value.lower()

        return value

    # pylint: enable=all

    # pylint: disable=all
    @property
    def tags(self) -> Dict[str, str]:
        """
        @property
        def tags(self) -> Dict[str, str]:
            Retrieves the tags associated with the resource.

            The method combines the default tags from the resource type with additional tags loaded from an external source,
            and returns the merged dictionary of tags.

            Returns:
                Dict[str, str]: A dictionary containing the combined tags.
        """
        tags: Dict[str, str] = self.resource_type.resource_tags if self.resource_type.resource_tags else {}
        tags = tags | Loader().tags.values
        return tags

    # pylint: enable=all

    @staticmethod
    def load_resource(logical_name: str, resource_description: str) -> Resource:
        """
        Loads a resource with the given logical name and type.

        Parameters:
        logical_name (str): The logical name of the resource.
        resource_description (str): The description of the resource.
        resource_type (ResourceType): The type of the resource.

        Returns:
        Resource: The loaded resource.

        Raises:
        ValueError: If the resource type is not specified or invalid.
        ValueError: If the logical name is not specified or empty.
        """
        if not logical_name or not logical_name.strip():
            raise ValueError("Resource name is required")

        resource: Resource = Resource(
            logical_name=logical_name,
            resource_description=resource_description,
            resource_name_pattern=constants.AWS_DEFAULT_RESOURCE_NAME_PATTERN,
        )

        return resource
