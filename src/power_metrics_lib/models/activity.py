"""Module for the activity model.

Examples:
    >>> from power_metrics_lib import Activity
    >>>
    >>> # Create an activity from the a .fit file:
    >>> file_path = "tests/files/activity.fit"
    >>> activity = Activity(file_path)
    >>>
    >>> # Set your FTP:
    >>> ftp: int = 300
    >>>
    >>> # Calculate all the metrics:
    >>> activity.calculate_metrics(ftp)
    >>>
    >>> # Check the metrics:
    >>> assert activity.metrics.duration == 7023
    >>> assert activity.metrics.average_power == 187.02520290474158
"""

from dataclasses import dataclass

from garmin_fit_sdk import Decoder, Stream

from .metrics import Metrics


@dataclass
class Activity:
    """Model for an activity.

    Attributes:
        timestamps (list[int]): The timestamps.
        power (list[int]): The power data.

    """

    def __init__(
        self,
        file_path: str | None = None,
        timestamps: list[int] | None = None,
        power: list[int] | None = None,
        ftp: int = 0,
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

        self.metrics = Metrics()

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

        self.calculate_metrics(ftp)

    timestamps: list[int]
    power: list[int]
    metrics: Metrics

    def calculate_metrics(self, ftp: int | None) -> None:
        """Calculate the metrics.

        Args:
            ftp: The functional threshold power.

        """
        self.metrics = Metrics(self.timestamps, self.power, ftp)

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
