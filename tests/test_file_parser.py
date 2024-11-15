"""Test module the file_parser.py module."""

import pytest

from power_metrics_lib.file_parsers import parse_fit_activity_file

TEST_FILE = "tests/files/file.fit"
EXPECTED_NO_OF_RECORDS = 7023


def test_parse_fit_activity_file() -> None:
    """Test the parse_fit_activity_file function."""
    parsed_data = parse_fit_activity_file(TEST_FILE)

    assert len(parsed_data) == EXPECTED_NO_OF_RECORDS
    assert isinstance(parsed_data, list)
    assert isinstance(parsed_data[0], dict)

    # Check that the first record has the expected keys:
    assert "timestamp" in parsed_data[0]
    assert "power" in parsed_data[0]

    # Check that the first record has the expected values:
    expected_timestamp = 1100178981
    expected_power = 106
    assert parsed_data[0]["timestamp"] == expected_timestamp
    assert parsed_data[0]["power"] == expected_power


def test_parse_fit_activity_file_file_not_found() -> None:
    """Test the parse_fit_activity_file function."""
    with pytest.raises(FileNotFoundError):
        parse_fit_activity_file("file_not_found.fit")


def test_parse_fit_activity_file_no_record_messages() -> None:
    """Test the parse_fit_activity_file function."""
    with pytest.raises(ValueError, match="No record messages found in the .fit file."):
        parse_fit_activity_file("tests/files/zwift_workout.fit")
