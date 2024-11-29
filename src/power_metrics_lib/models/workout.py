"""Module for the workout model.

Examples:
    >>> from power_metrics_lib import Workout
    >>>
    >>> # Set your FTP:
    >>> ftp = 200
    >>>
    >>> # Create a workout from the a .zwo file:
    >>> file_path = "tests/files/zwift_workout.zwo"
    >>>
    >>> # Create a workout object:
    >>> workout = Workout(file_path=file_path, ftp=ftp)
    >>>
    >>> # Check the metrics:
    >>> assert 3360 == workout.duration
    >>> assert 127 == round(workout.average_power, 0)
"""

from abc import ABC
from dataclasses import dataclass, field

from defusedxml.ElementTree import parse

from .activity import Activity


class UnsupportedFileTypeError(Exception):
    """Unsupported file type."""


@dataclass
class Block(ABC):
    """Model for a block.

    Attributes:
        duration (int): The duration of the block.
    """

    duration: int


@dataclass
class Ramp(Block):
    """Model for a ramp block.

    Attributes:
        start_power (float): The start power.
        end_power (float): The end power.
    """

    start_power: float
    end_power: float


@dataclass
class Warmup(Ramp):
    """Model for a warmup block."""


@dataclass
class Cooldown(Ramp):
    """Model for a cooldown block."""


@dataclass
class SteadyState(Block):
    """Model for a steady state block.

    Attributes:
        power (float): The power.
    """

    power: float


@dataclass
class Interval(Block):
    """Model for an interval block.

    Attributes:
        repeat (int): The number of times to repeat the interval.
        on_power (float): The power during the work interval.
        on_duration (int): The duration of the work interval.
        off_power (float): The power during the rest interval.
        off_duration (int): The duration of the rest interval.
    """

    repeat: int
    on_power: float
    on_duration: int
    off_power: float
    off_duration: int
    duration: int = field(init=False)

    def __post_init__(self) -> None:
        """Calculate the duration of the interval block."""
        self.duration = self.repeat * (self.on_duration + self.off_duration)


@dataclass
class FreeRide(Block):
    """Model for a free ride block."""


@dataclass
class Workout(Activity):
    """Model for a workout.

    Attributes:
        blocks (list[Block]): The blocks.
    """

    def __init__(
        self,
        file_path: str | None = None,
        blocks: list[Block] | None = None,
        ftp: int | None = None,
    ) -> None:
        """Initialize the workout."""
        super().__init__(ftp=ftp)

        self.blocks = []
        if blocks is not None:
            self.blocks = blocks

        if file_path is not None:
            self.parse_workout_file(file_path)

        if ftp is not None:
            self.create_activity_from_workout(ftp)
            super().calculate_metrics()

    blocks: list[Block] = field(default_factory=list)

    def create_activity_from_workout(self, ftp: int) -> None:  # noqa: C901
        """Converts a workout to an activity.

        Args:
            ftp: The functional threshold power.

        Returns:
            Activity: The workout as an activity.

        Raises:
            TypeError: If the block type is invalid.
        """
        timestamp = 1
        for block in self.blocks:
            if isinstance(block, Warmup | Cooldown | Ramp):
                # Calculate the power increase per second
                power_increase_per_second = (
                    block.end_power - block.start_power
                ) / block.duration
                for i in range(block.duration):
                    self.timestamps.append(timestamp)
                    power = block.start_power + i * power_increase_per_second
                    self.power.append(round(power * ftp if power > 0 else 0))
                    timestamp += 1
            elif isinstance(block, SteadyState):
                for _ in range(block.duration):
                    self.timestamps.append(timestamp)
                    self.power.append(round(block.power * ftp))
                    timestamp += 1
            elif isinstance(block, Interval):
                for _ in range(block.repeat):
                    for _ in range(block.on_duration):
                        self.timestamps.append(timestamp)
                        self.power.append(round(block.on_power * ftp))
                        timestamp += 1
                    for _ in range(block.off_duration):
                        self.timestamps.append(timestamp)
                        self.power.append(round(block.off_power * ftp))
                        timestamp += 1
            elif isinstance(block, FreeRide):
                pass
            else:
                msg = f"Invalid block type: {type(block)}"
                raise TypeError(msg) from None

    def parse_workout_file(self, file_path: str) -> None:
        """Parse a .zwo file and return a workout object.

        Args:
            file_path: The path to the .zwo file.

        Returns:
            Workout: the workout object.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If there are any errors parsing the .zwo file.

        """
        if file_path.endswith(".zwo"):
            pass
        else:
            file_type = file_path.split(".")[-1]
            msg = f"Unsupported file type: {file_type}"
            raise UnsupportedFileTypeError(msg)

        try:
            tree = parse(file_path)
        except FileNotFoundError as e:
            msg = f"File not found: {file_path}"
            raise FileNotFoundError(msg) from e

        root = tree.getroot()
        blocks = root.findall("./workout/*")

        for block in blocks:
            if block.tag == "SteadyState":
                power = float(block.attrib["Power"])
                duration = int(round(float(block.attrib["Duration"])))
                self.blocks.append(SteadyState(power=power, duration=duration))
            elif block.tag in ("Cooldown", "Warmup", "Ramp"):
                power_low = float(block.attrib["PowerLow"])
                power_high = float(block.attrib["PowerHigh"])
                duration = int(round(float(block.attrib["Duration"])))
                if block.tag == "Cooldown":
                    self.blocks.append(
                        Cooldown(
                            duration=duration,
                            start_power=power_low,
                            end_power=power_high,
                        )
                    )
                elif block.tag == "Warmup":
                    self.blocks.append(
                        Warmup(
                            duration=duration,
                            start_power=power_low,
                            end_power=power_high,
                        )
                    )
                else:
                    # "Ramp"
                    self.blocks.append(
                        Ramp(
                            duration=duration,
                            start_power=power_low,
                            end_power=power_high,
                        )
                    )
            elif block.tag == "IntervalsT":
                repeat = int(block.attrib["Repeat"])
                on_power = float(block.attrib["OnPower"])
                off_power = float(block.attrib["OffPower"])
                on_duration = int(round(float(block.attrib["OnDuration"])))
                off_duration = int(round(float(block.attrib["OffDuration"])))
                self.blocks.append(
                    Interval(
                        repeat=repeat,
                        on_power=on_power,
                        off_power=off_power,
                        on_duration=on_duration,
                        off_duration=off_duration,
                    )
                )
            elif block.tag == "FreeRide":
                duration = int(round(float(block.attrib["Duration"])))
                self.blocks.append(FreeRide(duration))
            else:
                msg = f"Unknown block type: {block.tag}"
                raise ValueError(msg) from None
