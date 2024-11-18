"""Test module the file_parser.py module."""

import pytest

from power_metrics_lib.file_parsers import (
    parse_fit_activity_file,
    parse_zwo_workout_file,
)


# Activity files:
def test_parse_fit_activity_file() -> None:
    """Test the parse_fit_activity_file function."""
    test_file = "tests/files/file.fit"
    expected_no_of_records = 7023

    workout_data = parse_fit_activity_file(test_file)

    assert len(workout_data) == expected_no_of_records
    assert isinstance(workout_data, list)
    assert isinstance(workout_data[0], dict)

    # Check that the first record has the expected keys:
    assert "timestamp" in workout_data[0]
    assert "power" in workout_data[0]

    # Check that the first record has the expected values:
    expected_timestamp = 1100178981
    expected_power = 106
    assert workout_data[0]["timestamp"] == expected_timestamp
    assert workout_data[0]["power"] == expected_power


def test_parse_fit_activity_file_file_not_found() -> None:
    """Test the parse_fit_activity_file function."""
    with pytest.raises(FileNotFoundError):
        parse_fit_activity_file("file_not_found.fit")


def test_parse_fit_activity_file_no_record_messages() -> None:
    """Test the parse_fit_activity_file function."""
    with pytest.raises(ValueError, match="No record messages found in the .fit file."):
        parse_fit_activity_file("tests/files/zwift_workout.fit")


# Workout files:


def test_parse_zwo_workout_file() -> None:
    """Test the parse_fit_activity_file function."""
    test_file = "tests/files/zwift_workout.zwo"
    expected_no_of_steps = 10

    workout_data = parse_zwo_workout_file(test_file)

    assert isinstance(workout_data, list)
    assert isinstance(workout_data[0], dict)
    assert len(workout_data) == expected_no_of_steps

    # Check that "step_type" is in all records:
    assert all("step_type" in d for d in workout_data)

def test_parse_zwo_workout_file_file_not_found() -> None:
    """Should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_zwo_workout_file("file_not_found.zwo")


def test_parse_zwo_workout_file_unknown_step_type() -> None:
    """Should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown step type: UnknownStepType"):
        parse_zwo_workout_file("tests/files/zwift_workout_unknown_step_type.zwo")
