"""Storage model."""

from __future__ import annotations

from pydantic import BaseModel


class Storage(BaseModel):
    """Represents a Storage model with different storage layers and zones.

    Attributes:
        first_layer (str | None): The first storage layer.
        second_layer (str | None): The second storage layer.
        third_layer (str | None): The third storage layer.
        landing_zone (str | None): The landing zone for the storage.
        assets (str | None): The assets in the storage.
    """

    first_layer: str | None  # type: ignore[annotation-unchecked]
    second_layer: str | None  # type: ignore[annotation-unchecked]
    third_layer: str | None  # type: ignore[annotation-unchecked]
    landing_zone: str | None  # type: ignore[annotation-unchecked]
    assets: str | None  # type: ignore[annotation-unchecked]
