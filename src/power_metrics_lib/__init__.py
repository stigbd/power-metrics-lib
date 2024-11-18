"""Package for the power-metrics-lib library.

This package provides a set of functions to calculate power based metrics.


Examples:
    >>> from power_metrics_lib.file_parsers import parse_activity_file
    >>> import power_metrics_lib.calculate_metrics as pm
    >>> from power_metrics_lib.models import Activity
    >>>
    >>> file_path = "tests/files/file.fit"
    >>> # Parse the .fit file:
    >>> activity: Activity = parse_activity_file(file_path)
    >>>
    >>> # Calculate the average power:
    >>> average_power: float = pm.calculate_average_power(activity.power)
    >>>
    >>> # Calculate the normalized power:
    >>> normalized_power: float = pm.calculate_normalized_power(activity.power)
    >>>
    >>> # Set your FTP:
    >>> ftp: int = 300
    >>>
    >>> # Calculate the intensity factor:
    >>> intensity_factor: float = pm.calculate_intensity_factor(
        normalized_power=normalized_power,
        ftp=ftp,
        )
    >>>
    >>> # Calculate the duration:
    >>> duration: dict[str, int |str ] = pm.calculate_duration(activity.power)
    >>>
    >>> # Calculate the training stress score:
    >>> training_stress_score: float = pm.calculate_training_stress_score(
        normalized_power=normalized_power,
        intensity_factor=intensity_factor,
        ftp=ftp,
        duration=duration["seconds"],
        )
"""
