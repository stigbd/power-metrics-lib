"""Integration test module for the Workout class."""

import pytest

from power_metrics_lib.models.workout import (
    Block,
    Cooldown,
    FreeRide,
    Interval,
    Ramp,
    SteadyState,
    Warmup,
    Workout,
)


def test_create_workout_from_file() -> None:
    """Should create a workout based on a file and generate all blocks correctly."""
    test_file = "tests/files/zwift_workout.zwo"
    expected_no_of_blocks = 10

    workout = Workout(file_path=test_file)

    assert isinstance(workout, Workout)
    assert expected_no_of_blocks == len(workout.blocks)


def test_create_workout_from_file_with_ftp() -> None:
    """Should create a workout based on a file and generate all blocks correctly."""
    test_file = "tests/files/zwift_workout.zwo"
    expected_no_of_blocks = 10
    ftp = 200
    expected_duration = 3630
    expected_average_power = 140
    expected_max_power = 300
    expected_normalized_power = 181
    expected_intensity_factor = 0.905
    expected_tss = 83
    expected_total_work = 508482

    workout = Workout(file_path=test_file, ftp=ftp)

    assert isinstance(workout, Workout)
    assert expected_no_of_blocks == len(workout.blocks)
    assert expected_duration == len(workout.timestamps)
    assert len(workout.power) == len(workout.timestamps)
    assert expected_duration == workout.metrics.duration
    assert expected_average_power == round(workout.metrics.average_power, 0)
    assert expected_max_power == workout.metrics.max_power
    assert expected_normalized_power == round(workout.metrics.normalized_power, 0)
    assert expected_intensity_factor == round(workout.metrics.intensity_factor, 3)
    assert expected_tss == round(workout.metrics.training_stress_score, 0)
    assert expected_total_work == workout.metrics.total_work


def test_create_workout() -> None:
    """Should return a valid activity object."""
    # Define the workout:
    warmup = Warmup(duration=300, start_power=0.60, end_power=0.80)
    steady_state = SteadyState(duration=300, power=0.80)
    interval = Interval(
        repeat=5, on_duration=30, on_power=1.0, off_duration=30, off_power=0.60
    )
    ramp = Ramp(duration=300, start_power=0.60, end_power=0.80)
    free_ride = FreeRide(duration=300)
    cooldown = Cooldown(duration=300, start_power=0.80, end_power=0.60)

    blocks = [warmup, steady_state, interval, ramp, free_ride, cooldown]
    # Define the FTP:
    ftp = 200

    workout = Workout(blocks=blocks, ftp=ftp)

    # Calculate the total duration of the workout,
    # excluding the free ride block:
    total_duration = sum(b.duration for b in blocks) - free_ride.duration

    # Check the timestamps:
    assert total_duration == len(workout.timestamps)
    assert is_strictly_incremental(workout.timestamps)
    assert workout.timestamps[0] == 1
    assert workout.timestamps[-1] == total_duration

    # Check the power data:
    assert total_duration == len(workout.power)
    assert workout.power[0] == warmup.start_power * ftp
    assert workout.power[299] == warmup.end_power * ftp
    assert workout.power[300] == steady_state.power * ftp
    assert workout.power[599] == steady_state.power * ftp
    assert workout.power[600] == interval.on_power * ftp
    assert workout.power[629] == interval.on_power * ftp
    assert workout.power[630] == interval.off_power * ftp
    assert workout.power[659] == interval.off_power * ftp
    assert workout.power[1200] == cooldown.start_power * ftp
    assert workout.power[-1] == cooldown.end_power * ftp

    # Check that the power data is incremental or decremental
    # for the warmup and cooldown blocks:
    assert is_incremental(workout.power[:300])
    assert is_decremental(workout.power[1200:-1])


def test_create_workout_with_abstract_block() -> None:
    """Should raise a TypeError for an invalid block type."""
    with pytest.raises(TypeError, match="Invalid block type"):
        Workout(blocks=[Block(duration=300)], ftp=200)


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
