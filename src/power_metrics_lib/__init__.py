"""Package for the power-metrics-lib library.

This package provides a set of functions to calculate power based metrics.


Examples:
    >>> from power_metrics_lib import Activity
    >>>
    >>> file_path = "tests/files/file.fit"
    >>> # Parse the .fit file:
    >>> activity: Activity = Activity(file_path)
    >>>
    >>> # Set your FTP:
    >>> ftp: int = 300
    >>>
    >>> # Calculate all the metrics:
    >>> activity.calculate_metrics(ftp)
    >>> # Check the metrics:
    >>> assert activity.metrics.duration == 7023
    >>> assert activity.metrics.average_power == 187.02520290474158
"""

from .models import Activity, Metrics, Workout

__all__ = ["Activity", "Metrics", "Workout"]
