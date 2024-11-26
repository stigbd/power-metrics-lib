"""This module contains the model for the metrics."""

from dataclasses import dataclass

from power_metrics_lib.calculate_metrics import (
    calculate_average_power,
    calculate_duration,
    calculate_intensity_factor,
    calculate_max_power,
    calculate_normalized_power,
    calculate_total_work,
    calculate_training_stress_score,
)


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
        if timestamps and power:
            self.duration = calculate_duration(timestamps)
            self.average_power = calculate_average_power(power)
            self.normalized_power = calculate_normalized_power(power)
            self.max_power = calculate_max_power(power)

        if timestamps and power and ftp:
            self.intensity_factor = calculate_intensity_factor(
                self.normalized_power, ftp
            )
            self.training_stress_score = calculate_training_stress_score(
                self.normalized_power, self.intensity_factor, ftp, self.duration
            )
            self.total_work = calculate_total_work(power)
        else:
            return

    duration: int = 0
    average_power: float = 0
    normalized_power: float = 0
    max_power: int = 0
    intensity_factor: float = 0
    training_stress_score: float = 0
    total_work: int = 0
