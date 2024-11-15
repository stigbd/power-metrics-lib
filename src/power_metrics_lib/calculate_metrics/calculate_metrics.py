"""Module to calculate power based metrics."""

from datetime import timedelta

import pandas as pd


def calculate_average_power(power_data: list[int]) -> float:
    """Calculate the average power from a list of power data.

    Args:
        power_data (list[int]): A list of power data.

    Returns:
        float: The average power.

    Examples:
        >>> calculate_average_power([100, 200, 300, 400, 500])
        300.0
    """
    return sum(power_data) / len(power_data)


def calculate_normalized_power(power_data: list[int], window_size: int = 30) -> float:
    """Calculate the normalized power from a list of power data.

    Args:
        power_data (list[int]): A list of power data.
        window_size (int): The window size for the rolling mean.

    Returns:
        float: The normalized power.

    Examples:
        >>> calculate_normalized_power([100, 200, 300, 400, 500], window_size = 3)
        329.0
    """
    series = pd.Series(power_data)
    series = series.dropna()
    windows = series.rolling(window_size)
    power_30s = windows.mean()

    return round((((power_30s**4).mean()) ** 0.25), 0).item()


def calculate_intensity_factor(normalized_power: float, ftp: float) -> float:
    """Calculate the intensity factor from normalized power and FTP.

    Args:
        normalized_power (float): The normalized power.
        ftp (float): The functional threshold power.

    Returns:
        float: The intensity factor.

    Examples:
        >>> calculate_intensity_factor(normalized_power = 300, ftp = 200)
        1.5
    """
    return normalized_power / ftp


def calculate_training_stress_score(
    normalized_power: float,
    intensity_factor: float,
    ftp: float,
    duration: float,
) -> float:
    """Calculate the training stress score from normalized power, FTP and duration.

    Args:
        normalized_power (float): The normalized power.
        intensity_factor (float): The intensity factor.
        ftp (float): The functional threshold power.
        duration (float): The duration in seconds.

    Returns:
        float: The training stress score.

    Examples:
        >>> calculate_training_stress_score(
            normalized_power = 300,
            ftp = 200, duration = 3600,
            intensity_factor = 1.5)
        225.0
    """
    return (normalized_power * intensity_factor * duration) / (ftp * 3600) * 100


def calculate_total_work(power_data: list[int]) -> float:
    """Calculate the total work from power data.

    Args:
        power_data (list[int]): A list of power data.

    Returns:
        float: The total work.

    Examples:
        >>> calculate_total_work([100, 200, 300, 400, 500])
        1500
    """
    return sum(power_data)


def calculate_max_power(power_data: list[int]) -> float:
    """Calculate the max power from power data.

    Args:
        power_data (list[int]): A list of power data.

    Returns:
        float: The max power.

    Examples:
        >>> calculate_max_power([100, 200, 300, 400, 500])
        500
    """
    return max(power_data)


def calculate_duration(power_data: list[int]) -> dict[str, int | str]:
    """Calculate the duration from power data.

    Args:
        power_data (list[int]): A list of power data.

    Returns:
        dict[str, int | str]: The duration in seconds and hh:mm:ss format.

    Examples:
        >>> calculate_duration([100, 200, 300, 400, 500])
        {'seconds': 5, 'hh:mm:ss': '0:00:05'}
    """
    return {
        "seconds": len(power_data),
        "hh:mm:ss": str(timedelta(seconds=len(power_data))),
    }
