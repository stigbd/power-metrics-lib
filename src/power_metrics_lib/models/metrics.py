"""This module contains the model for the metrics."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class Metrics:
    """Model for all the metrics.

    Attributes:
        duration (int): The duration.
        average_power (float): The average power.
        normalized_power (float): The normalized power.
        max_power (int): The max power.
        intensity_factor (float): The intensity factor.
        training_stress_score (float): The training stress score.
        total_work (int): The total work.
    """

    def __init__(
        self,
        timestamps: list[int] | None = None,
        power: list[int] | None = None,
        ftp: int | None = None,
    ) -> None:
        """Initialize the metrics.

        Args:
            timestamps: The timestamps.
            power: The power data.
            ftp: The functional threshold power.

        """
        self.calculate_duration(timestamps)
        self.calculate_average_power(power)
        self.calculate_normalized_power(power)
        self.calculate_max_power(power)
        self.calculate_intensity_factor(self.normalized_power, ftp)
        self.calculate_training_stress_score(
            self.normalized_power, self.intensity_factor, ftp, self.duration
        )
        self.calculate_total_work(power)

    duration: int = 0
    average_power: float = 0
    normalized_power: float = 0
    max_power: int = 0
    intensity_factor: float = 0
    training_stress_score: float = 0
    total_work: int = 0

    def calculate_average_power(self, power_data: list[int] | None) -> None:
        """Calculate the average power from a list of power data.

        Args:
            power_data (list[int]): A list of power data.

        """
        if power_data:
            self.average_power = sum(power_data) / len(power_data)

    def calculate_normalized_power(
        self, power_data: list[int] | None, window_size: int = 30
    ) -> None:
        """Calculate the normalized power from a list of power data.

        Args:
            power_data (list[int]): A list of power data.
            window_size (int): The window size for the rolling mean.

        """
        if not power_data:
            return

        if len(power_data) < window_size:
            return

        series = pd.Series(power_data)
        series = series.dropna()
        windows = series.rolling(window_size)
        power_30s = windows.mean()

        self.normalized_power = round((((power_30s**4).mean()) ** 0.25), 0).item()

    def calculate_intensity_factor(
        self, normalized_power: float | None, ftp: float | None
    ) -> None:
        """Calculate the intensity factor from normalized power and FTP.

        Args:
            normalized_power (float): The normalized power.
            ftp (float): The functional threshold power.

        """
        if normalized_power and ftp:
            self.intensity_factor = normalized_power / ftp

    def calculate_training_stress_score(
        self,
        normalized_power: float | None,
        intensity_factor: float | None,
        ftp: float | None,
        duration: float | None,
    ) -> None:
        """Calculate the training stress score from normalized power, FTP and duration.

        Args:
            normalized_power (float): The normalized power.
            intensity_factor (float): The intensity factor.
            ftp (float): The functional threshold power.
            duration (float): The duration in seconds.

        """
        if normalized_power and intensity_factor and ftp and duration:
            self.training_stress_score = (
                (normalized_power * intensity_factor * duration) / (ftp * 3600) * 100
            )

    def calculate_total_work(self, power_data: list[int] | None) -> None:
        """Calculate the total work from power data.

        Args:
            power_data (list[int]): A list of power data.
        """
        if power_data:
            self.total_work = sum(power_data)

    def calculate_max_power(self, power_data: list[int] | None) -> None:
        """Calculate the max power from power data.

        Args:
            power_data (list[int]): A list of power data.

        """
        if power_data:
            self.max_power = max(power_data)

    def calculate_duration(self, timestamps: list[int] | None) -> None:
        """Calculate the duration from power data.

        Args:
            timestamps (list[int]): A list of timestamps.

        """
        if timestamps:
            self.duration = len(timestamps)
