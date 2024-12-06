"""Integration test module for the Workout class."""

import pytest

from power_metrics_lib.models.workout import (
    Block,
    Cooldown,
    FreeRide,
    Interval,
    Ramp,
    SteadyState,
    UnsupportedFileTypeError,
    Warmup,
    Workout,
)

EXPECTED_NO_OF_BLOCKS = 10
FTP = 200
EXPECTED_DURATION = 3360
EXPECTED_AVERAGE_POWER = 127
EXPECTED_MAX_POWER = 300
EXPECTED_NORMALIZED_POWER = 150
EXPECTED_INTENSITY_FACTOR = 0.75
EXPECTED_TSS = 52
EXPECTED_TOTAL_WORK = 427482
EXPECTED_VARIABILITY_INDEX = 1.178997010400438


def test_create_workout_from_file_no_ftp() -> None:
    """Shold create a workout with only blocks."""
    test_file = "tests/files/zwift_workout.zwo"

    workout = Workout(file_path=test_file)

    assert isinstance(workout, Workout)
    assert len(workout.blocks) == EXPECTED_NO_OF_BLOCKS
    assert workout.timestamps == []
    assert workout.power == []
    assert workout.duration == 0
    assert workout.average_power == 0
    assert workout.normalized_power == 0
    assert workout.max_power == 0
    assert workout.intensity_factor == 0
    assert workout.training_stress_score == 0
    assert workout.total_work == 0


def test_create_workout_from_zwo_file() -> None:
    """Should create a workout based on a file and generate all blocks correctly."""
    test_file = "tests/files/zwift_workout.zwo"

    workout = Workout(file_path=test_file, ftp=FTP)

    assert isinstance(workout, Workout)
    assert len(workout.blocks) == EXPECTED_NO_OF_BLOCKS
    assert len(workout.timestamps) == EXPECTED_DURATION
    assert len(workout.power) == len(workout.timestamps)
    assert workout.duration == EXPECTED_DURATION
    assert round(workout.average_power, 0) == EXPECTED_AVERAGE_POWER
    assert workout.max_power == EXPECTED_MAX_POWER
    assert round(workout.normalized_power, 0) == EXPECTED_NORMALIZED_POWER
    assert round(workout.intensity_factor, 3) == EXPECTED_INTENSITY_FACTOR
    assert round(workout.training_stress_score, 0) == EXPECTED_TSS
    assert workout.total_work == EXPECTED_TOTAL_WORK
    assert workout.ftp == FTP
    assert workout.variability_index == EXPECTED_VARIABILITY_INDEX
    assert len(workout.power_duration_curve) == len(workout.timestamps)
    assert workout.power_duration_curve[0] == workout.max_power
    assert workout.power_profile == {
        5: workout.power_duration_curve[5 - 1],
        1 * 60: workout.power_duration_curve[(1 * 60) - 1],
        5 * 60: workout.power_duration_curve[(5 * 60) - 1],
        20 * 60: workout.power_duration_curve[(20 * 60) - 1],
    }
    # The workout duration is < 60 minutes, so the 60 minute power is not included:
    assert 60 * 60 not in workout.power_profile


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


def test_create_workout_with_invalid_block() -> None:
    """Should raise a TypeError for an invalid block type."""
    test_file = "tests/files/zwift_workout_unknown_block_type.zwo"

    with pytest.raises(ValueError, match="Unknown block type"):
        Workout(file_path=test_file)


def test_create_workout_with_file_not_found() -> None:
    """Should raise a FileNotFoundError."""
    test_file = "file_that_does_not_exist.zwo"

    with pytest.raises(
        FileNotFoundError, match="File not found: file_that_does_not_exist.zwo"
    ):
        Workout(file_path=test_file)


def test_create_workout_with_unsupported_file_format() -> None:
    """Should raise unsupported file format error."""
    test_file = "tests/files/unsupported_file_format.txt"

    with pytest.raises(UnsupportedFileTypeError, match="Unsupported file type: txt"):
        Workout(file_path=test_file)


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
