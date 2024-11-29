"""Package for the power-metrics-lib library.

This library provides a set of functions to calculate power based metrics from
either an activity file or a workout.
"""

from .models import Activity, Workout

__all__ = ["Activity", "Workout"]
