"""Module for the workout model."""

from abc import ABC
from dataclasses import dataclass, field


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
        work_power: The power during the work interval.
        work_duration: The duration of the work interval.
        rest_power: The power during the rest interval.
        rest_duration: The duration of the rest interval.
    """

    repeat: int
    work_power: float
    work_duration: int
    rest_power: float
    rest_duration: int
    duration: int = field(init=False)

    def __post_init__(self) -> None:
        """Calculate the duration of the interval block."""
        self.duration = self.repeat * (self.work_duration + self.rest_duration)


@dataclass
class FreeRide(Block):
    """Model for a free ride block."""


@dataclass
class Workout:
    """Model for a workout.

    Attributes:
        blocks: The blocks.
    """

    blocks: list[Block]
