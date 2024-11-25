"""Module for the workout model."""

from abc import ABC
from dataclasses import dataclass, field

from power_metrics_lib.file_parsers import parse_workout_file

from .activity import Activity


@dataclass
class Block(ABC):
    """Model for a block.

    Attributes:
        duration: The duration of the block.
    """

    duration: int


@dataclass
class Ramp(Block):
    """Model for a ramp block.

    Attributes:
        start_power: The start power.
        end_power: The end power.
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
        power: The power.
    """

    power: float


@dataclass
class Interval(Block):
    """Model for an interval block.

    Attributes:
        repeat: The number of times to repeat the interval.
        on_power: The power during the work interval.
        on_duration: The duration of the work interval.
        off_power: The power during the rest interval.
        off_duration: The duration of the rest interval.
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
        blocks: The blocks.
    """

    def __init__(  # noqa: C901
        self,
        file_path: str | None = None,
        blocks: list[Block] | None = None,
        ftp: int | None = None,
    ) -> None:
        """Initialize the workout."""
        super().__init__()

        self.blocks = []
        if blocks is not None:
            self.blocks = blocks

        if file_path is not None:
            _blocks: list[dict] = parse_workout_file(file_path)

            for block in _blocks:
                if "SteadyState" in block:
                    self.blocks.append(SteadyState(**block["SteadyState"]))
                elif "Warmup" in block:
                    self.blocks.append(Warmup(**block["Warmup"]))
                elif "Cooldown" in block:
                    self.blocks.append(Cooldown(**block["Cooldown"]))
                elif "Interval" in block:
                    self.blocks.append(Interval(**block["Interval"]))
                elif "Ramp" in block:
                    self.blocks.append(Ramp(**block["Ramp"]))
                elif "FreeRide" in block:
                    self.blocks.append(FreeRide(**block["FreeRide"]))
                else:  # pragma: no cover
                    msg = "Invalid block type."
                    raise TypeError(msg)

        if ftp is not None:
            self.create_activity_from_workout(ftp)
            super().calculate_metrics(ftp)

    blocks: list[Block]

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
                    for _ in range(block.off_duration):
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
