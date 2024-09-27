# mypy: ignore-errors
from __future__ import annotations

from pydantic import BaseModel


class Company(BaseModel):
    """
    This module contains the definition of the `Company` class.

    Classes:
    - `Company`: A class that represents a company.

    Attributes:
    - `name` (str): The name of the company.
    - `short_name` (str): The short name of the company.

    Example:
    ```
    from module_name import Company

    # Create a new company
    company = Company()

    # Set the name, short name and team of the company
    company.name = "ABC Company"
    company.short_name = "ABC"
    ```
    """

    name: str
    short_name: str
