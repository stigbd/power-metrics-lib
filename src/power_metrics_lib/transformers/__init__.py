"""Module for transforming data into a format that can be used by the model."""

from .workout_to_activity import transform_workout_to_activity

__all__ = ["transform_workout_to_activity"]
