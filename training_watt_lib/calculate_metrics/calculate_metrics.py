"""Module to calculate power based metrics."""

from datetime import timedelta

import pandas as pd


def calculate_average_power(power_data: list[int]) -> float:
    """Calculate the average power from a list of power data."""
    return sum(power_data) / len(power_data)


def calculate_normalised_power(power_data: list[int], window_size: int = 30) -> float:
    """Calculate the normalised power from a list of power data."""
    series = pd.Series(power_data)
    series = series.dropna()
    windows = series.rolling(window_size)
    power_30s = windows.mean()

    return round((((power_30s**4).mean()) ** 0.25), 0)


def calculate_intensity_factor(normalised_power: float, ftp: float) -> float:
    """Calculate the intensity factor from normalised power and FTP."""
    return normalised_power / ftp


def calculate_training_stress_score(
    normalised_power: float, ftp: float, duration: float
) -> float:
    """Calculate the training stress score from normalised power, FTP and duration."""
    intensity_factor = calculate_intensity_factor(normalised_power, ftp)
    return (normalised_power * intensity_factor * duration) / (ftp * 3600) * 100


def calculate_total_work(power_data: list[int]) -> float:
    """Calculate the total work from power data."""
    return sum(power_data)


def calculate_max_power(power_data: list[int]) -> float:
    """Calculate the max power from power data."""
    return max(power_data)


def calculate_duration(power_data: list[int]) -> dict[str, int | str]:
    """Calculate the duration from power data."""
    return {
        "seconds": len(power_data),
        "hh:mm:ss": str(timedelta(seconds=len(power_data))),
    }
