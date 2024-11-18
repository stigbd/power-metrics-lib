"""Package for the fit file parser module."""

from .fit_file_parser import parse_fit_activity_file
from .zwo_file_parser import parse_zwo_workout_file

__all__ = ["parse_fit_activity_file", "parse_zwo_workout_file"]
