"""Unit test module the file_parser.py module."""

import pytest

from power_metrics_lib.file_parsers import parse_workout_file


def test_parse_workout_file() -> None:
    """Should return a workout object."""
    test_file = "tests/files/zwift_workout.zwo"
    expected_no_of_blocks = 10

    workout = parse_workout_file(test_file)

    assert isinstance(workout, list)
    assert len(workout) == expected_no_of_blocks


def test_parse_workout_file_file_not_found() -> None:
    """Should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_workout_file("file_not_found.zwo")


def test_parse_workout_file_unknown_block_type() -> None:
    """Should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown block type: UnknownBlockType"):
        parse_workout_file("tests/files/zwift_workout_unknown_block_type.zwo")
