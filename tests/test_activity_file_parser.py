"""Test module the file_parser.py module."""

import pytest

from power_metrics_lib.file_parsers import parse_activity_file
from power_metrics_lib.models import Activity


# Activity files:
def test_parse_activity_file() -> None:
    """Test the parse_activity_file function."""
    test_file = "tests/files/file.fit"

    activity = parse_activity_file(test_file)

    assert isinstance(activity, Activity)

    # Check that the first record has the expected values:
    expected_timestamp = 1100178981
    expected_power = 106
    assert activity.timestamps[0] == expected_timestamp
    assert activity.power[0] == expected_power


def test_parse_activity_file_file_not_found() -> None:
    """Test the parse_activity_file function."""
    with pytest.raises(FileNotFoundError):
        parse_activity_file("file_not_found.fit")


def test_parse_activity_file_no_record_messages() -> None:
    """Test the parse_activity_file function."""
    with pytest.raises(ValueError, match="No record messages found in the .fit file."):
        parse_activity_file("tests/files/zwift_workout.fit")
