"""Package for the power-metrics-lib library.

This package provides a set of functions to calculate power based metrics.


Examples:
    >>> from power_metrics_lib.fit_file_parser import parse_fit_file
    >>> import power_metrics_lib.calculate_metrics as pm
    >>>
    >>> file_path = "tests/files/file.fit"
    >>> # Parse the .fit file:
    >>> activity_data: list[dict] = parse_fit_file(file_path)
    >>>
    >>> # Extract the power data from the activity data:
    >>> power_data: list[int] = [d["power"] for d in activity_data]
    >>>
    >>> # Calculate the average power:
    >>> average_power: float = pm.calculate_average_power(power_data)
    >>>
    >>> # Calculate the normalized power:
    >>> normalized_power: float = pm.calculate_normalized_power(power_data)
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
    >>> duration: dict[str, int |str ] = pm.calculate_duration(power_data)
    >>>
    >>> # Calculate the training stress score:
    >>> training_stress_score: float = pm.calculate_training_stress_score(
        normalized_power=normalized_power,
        intensity_factor=intensity_factor,
        ftp=ftp,
        duration=duration["seconds"],
        )
"""
