"""Module for the activity model."""

from dataclasses import dataclass

from power_metrics_lib.file_parsers import parse_activity_file

from .metrics import Metrics


@dataclass
class Activity:
    """Model for an activity.

    Attributes:
        timestamps: The timestamps.
        power: The power data.

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
            record_messages = parse_activity_file(file_path)
            for timestamp in [m["timestamp"] for m in record_messages]:
                self.timestamps.append(int(timestamp))

            for p in [m["power"] for m in record_messages]:
                self.power.append(int(p))

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
