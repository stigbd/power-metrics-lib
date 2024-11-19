"""Module for the activity model."""

from dataclasses import dataclass


@dataclass
class Activity:
    """Model for an activity.

    Attributes:
        timestamps: The timestamps.
        power: The power data.

    """

    timestamps: list[int]
    power: list[int]
