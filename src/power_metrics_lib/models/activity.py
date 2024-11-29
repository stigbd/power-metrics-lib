"""Module for the activity model.

Examples:
    >>> from power_metrics_lib import Activity
    >>>
    >>> # Parse the .fit file:
    >>> file_path = "tests/files/activity.fit"
    >>>
    >>> # Set your FTP:
    >>> ftp: int = 226
    >>>
    >>> # Create an activity object:
    >>> activity = Activity(file_path, ftp=ftp)
    >>>
    >>> # Check the metrics:
    >>> assert activity.duration == 7023
    >>> assert activity.average_power == 187.02520290474158
"""

from dataclasses import dataclass

import pandas as pd
from garmin_fit_sdk import Decoder, Stream


@dataclass
class Activity:
    """Model for an activity.

    Attributes:
        timestamps (list[int]): The timestamps.
        power (list[int]): The power data.

    """

    DEFAULT_WINDOW_SIZE = 30

    def __init__(
        self,
        file_path: str | None = None,
        timestamps: list[int] | None = None,
        power: list[int] | None = None,
        ftp: int | None = None,
        window_size: int | None = None,
    ) -> None:
        """Initialize the activity object."""
        if timestamps is None:
            self.timestamps = []
        else:
            self.timestamps = timestamps

        if power is None:
            self.power = []
        else:
            self.power = power

        self.ftp = ftp
        self.window_size = window_size or self.DEFAULT_WINDOW_SIZE

        if file_path:
            self.parse_activity_file(file_path)

        # Validate the timestamps and power data:
        # all timestamps must be strictly positive:
        if any(t <= 0 for t in self.timestamps):
            msg = "Timestamps must be positive."
            raise ValueError(msg) from None
        # all power data must greater or equal to zero:
        if any(p < 0 for p in self.power):
            msg = "Power data greater than or equal to zero."
            raise ValueError(msg) from None

        self.calculate_metrics()

    timestamps: list[int]
    power: list[int]
    ftp: int | None
    window_size: int
    # metrics:
    duration: int = 0
    average_power: float = 0
    normalized_power: float = 0
    max_power: int = 0
    intensity_factor: float = 0
    training_stress_score: float = 0
    total_work: int = 0
    variability_index: float = 0

    def calculate_metrics(self) -> None:
        """Calculate the metrics."""
        self.calculate_duration()
        self.calculate_average_power()
        self.calculate_normalized_power()
        self.calculate_max_power()
        self.calculate_intensity_factor()
        self.calculate_training_stress_score()
        self.calculate_total_work()
        self.calculate_variability_index()

    def parse_activity_file(self, file_path: str) -> None:
        """Parse a .fit file and return a list of dicts.

        Args:
            file_path: The path to the .fit file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If there are any errors parsing the .fit file.
        """
        try:
            stream = Stream.from_file(file_path)
        except FileNotFoundError as e:
            msg = f"File not found: {file_path}"
            raise FileNotFoundError(msg) from e

        decoder = Decoder(stream)
        messages, errors = decoder.read(
            convert_datetimes_to_dates=False,
            convert_types_to_strings=True,
        )

        if len(errors) > 0:  # pragma: no cover
            msg = "\n".join(errors)
            raise ValueError(msg) from None

        if "record_mesgs" not in messages:
            msg = "No record messages found in the .fit file."
            raise ValueError(msg) from None

        for message in messages["record_mesgs"]:
            self.timestamps.append(int(message["timestamp"]))
            self.power.append(int(message["power"]))

    def calculate_average_power(self) -> None:
        """Calculate the average power from a list of power data."""
        if self.power:
            self.average_power = sum(self.power) / len(self.power)

    def calculate_normalized_power(self) -> None:
        """Calculate the normalized power from a list of power data."""
        if not self.power:
            return

        if len(self.power) < self.window_size:
            return

        series = pd.Series(self.power)
        series = series.dropna()
        windows = series.rolling(self.window_size)
        power_30s = windows.mean()

        self.normalized_power = round((((power_30s**4).mean()) ** 0.25), 0).item()

    def calculate_intensity_factor(self) -> None:
        """Calculate the intensity factor from normalized power and FTP."""
        if self.normalized_power and self.ftp:
            self.intensity_factor = self.normalized_power / self.ftp

    def calculate_training_stress_score(self) -> None:
        """Calculate the training stress score."""
        if (
            self.normalized_power
            and self.intensity_factor
            and self.ftp
            and self.duration
        ):
            self.training_stress_score = (
                (self.normalized_power * self.intensity_factor * self.duration)
                / (self.ftp * 3600)
                * 100
            )

    def calculate_total_work(self) -> None:
        """Calculate the total work from power data."""
        if self.power:
            self.total_work = sum(self.power)

    def calculate_max_power(self) -> None:
        """Calculate the max power from power data."""
        if self.power:
            self.max_power = max(self.power)

    def calculate_duration(self) -> None:
        """Calculate the duration from timestamps."""
        if self.timestamps:
            self.duration = len(self.timestamps)

    def calculate_variability_index(self) -> None:
        """Calculate the variablity index."""
        if self.normalized_power and self.average_power:
            self.variability_index = self.normalized_power / self.average_power
