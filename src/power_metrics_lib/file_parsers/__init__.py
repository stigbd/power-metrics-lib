"""Package for the fit file parser module."""

from .activity_file_parser import parse_activity_file
from .workout_file_parser import parse_workout_file

__all__ = ["parse_activity_file", "parse_workout_file"]
