"""Module for testing the transform_workout_to_activity function."""

import pytest

from power_metrics_lib.models import (
    Activity,
    Block,
    Cooldown,
    Interval,
    Ramp,
    SteadyState,
    Warmup,
    Workout,
)
from power_metrics_lib.models.workout import FreeRide
from power_metrics_lib.transformers import transform_workout_to_activity


def test_transform_workout_to_activity() -> None:
    """Should return a valid activity object."""
    # Define the workout:
    warmup = Warmup(duration=300, start_power=0.60, end_power=0.80)
    steady_state = SteadyState(duration=300, power=0.80)
    interval = Interval(
        repeat=5, work_duration=30, work_power=1.0, rest_duration=30, rest_power=0.60
    )
    ramp = Ramp(duration=300, start_power=0.60, end_power=0.80)
    free_ride = FreeRide(duration=300)
    cooldown = Cooldown(duration=300, start_power=0.80, end_power=0.60)

    blocks = [warmup, steady_state, interval, ramp, free_ride, cooldown]
    workout = Workout(blocks=blocks)

    # Calculate the total duration of the workout,
    # excluding the free ride block:
    total_duration = sum(b.duration for b in blocks) - free_ride.duration

    # Define the FTP:
    ftp = 200

    activity = transform_workout_to_activity(workout=workout, ftp=ftp)

    # Check the return type:
    assert isinstance(activity, Activity)

    # Check the timestamps:
    assert total_duration == len(activity.timestamps)
    assert is_strictly_incremental(activity.timestamps)
    assert activity.timestamps[0] == 1
    assert activity.timestamps[-1] == total_duration

    # Check the power data:
    assert total_duration == len(activity.power)
    assert activity.power[0] == warmup.start_power * ftp
    assert activity.power[299] == warmup.end_power * ftp
    assert activity.power[300] == steady_state.power * ftp
    assert activity.power[599] == steady_state.power * ftp
    assert activity.power[600] == interval.work_power * ftp
    assert activity.power[629] == interval.work_power * ftp
    assert activity.power[630] == interval.rest_power * ftp
    assert activity.power[659] == interval.rest_power * ftp
    assert activity.power[1200] == cooldown.start_power * ftp
    assert activity.power[-1] == cooldown.end_power * ftp

    # Check that the power data is incremental or decremental
    # for the warmup and cooldown blocks:
    assert is_incremental(activity.power[:300])
    assert is_decremental(activity.power[1200:-1])


def test_transform_workout_to_activity_invalid_block() -> None:
    """Should raise a ValueError for an invalid block type."""
    blocks = [Block(duration=300)]
    workout = Workout(blocks=blocks)

    # Define the FTP:
    ftp = 200

    with pytest.raises(TypeError, match=f"Invalid block type: {type(blocks[0])}"):
        transform_workout_to_activity(workout=workout, ftp=ftp)


# Helper functions:
def is_strictly_incremental(lst: list[int]) -> bool:
    """Check if a list is incremental."""
    return lst == list(range(lst[0], lst[0] + len(lst)))


def is_incremental(lst: list[int]) -> bool:
    """Check if a list is incremental."""
    return all(lst[x] <= lst[x + 1] for x in range(len(lst) - 1))


def is_decremental(lst: list[int]) -> bool:
    """Check if a list is decremental."""
    return all(lst[x] >= lst[x + 1] for x in range(len(lst) - 1))
