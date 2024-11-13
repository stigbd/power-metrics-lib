"""Module to calculate power based metrics."""

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


def calcuate_intensity_factor(normalised_power: float, ftp: float) -> float:
    """Calculate the intensity factor from normalised power and FTP."""
    return normalised_power / ftp


def calculate_training_stress_score(
    normalised_power: float, ftp: float, duration: float
) -> float:
    """Calculate the training stress score from normalised power, FTP and duration."""
    intensity_factor = calcuate_intensity_factor(normalised_power, ftp)
    return (normalised_power * intensity_factor * duration) / (ftp * 3600) * 100


def calcuate_total_work(power_data: list[int]) -> float:
    """Calculate the total work from power data."""
    return sum(power_data)
