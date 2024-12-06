"""Integration tests for the Activity class."""

import pytest

from power_metrics_lib.models import Activity


def test_create_activity_from_file() -> None:
    """Should create an activity based on a file and generate all metrics correctly."""
    ftp = 236
    expected_duration = 7023
    expected_timestamp_first_record = 1100178981
    expected_power_first_record = 106
    expected_avgerage_power = 187.02520290474158
    expected_max_power = 289
    expected_normalized_power = 204.0
    expected_intensity_factor = 0.864406779661017
    expected_training_stress_score = 145.76608733122666
    expected_total_work = 1313478
    expected_variability_index = 1.0907620835674445

    activity = Activity(file_path="tests/files/activity.fit", ftp=ftp)

    assert isinstance(activity, Activity)

    # Check that the first record has the expected values:
    assert expected_timestamp_first_record == activity.timestamps[0]
    assert expected_power_first_record == activity.power[0]

    # Check that all the metrics are generated correctly
    assert expected_duration == activity.duration
    assert expected_avgerage_power == activity.average_power
    assert expected_normalized_power == activity.normalized_power
    assert expected_max_power == activity.max_power
    assert expected_intensity_factor == activity.intensity_factor
    assert expected_training_stress_score == activity.training_stress_score
    assert expected_total_work == activity.total_work
    assert expected_variability_index == activity.variability_index
    assert activity.window_size == Activity.DEFAULT_WINDOW_SIZE
    assert len(activity.power_duration_curve) == len(activity.timestamps)
    assert activity.power_duration_curve[0] == activity.max_power
    assert activity.power_profile == {
        5: activity.power_duration_curve[5 - 1],
        1 * 60: activity.power_duration_curve[(1 * 60) - 1],
        5 * 60: activity.power_duration_curve[(5 * 60) - 1],
        20 * 60: activity.power_duration_curve[(20 * 60) - 1],
        60 * 60: activity.power_duration_curve[(60 * 60) - 1],
    }


def test_create_activity_with_non_positive_timestamps() -> None:
    """Should raise a ValueError when the timestamps are not strictly positive."""
    ftp = 236

    with pytest.raises(ValueError, match="Timestamps must be positive"):
        Activity(timestamps=[0, 1, 2], ftp=ftp)


def test_create_activity_with_non_positive_power() -> None:
    """Should raise a ValueError when the power values are negative."""
    ftp = 236

    with pytest.raises(ValueError, match="Power data greater than or equal to zero"):
        Activity(power=[-1, 1, 2], ftp=ftp)


def test_parse_activity_file_file_not_found() -> None:
    """Test the parse_activity_file function."""
    with pytest.raises(FileNotFoundError):
        Activity(file_path="file_not_found.fit")


def test_parse_activity_file_no_record_messages() -> None:
    """Test the parse_activity_file function."""
    with pytest.raises(ValueError, match="No record messages found in the .fit file."):
        Activity(file_path="tests/files/zwift_workout.fit")


def test_create_activity_with_window_size_greater_than_power_data() -> None:
    """Should result in 0 normalized power."""
    activity = Activity(power=[100, 200, 300], window_size=4)
    assert activity.normalized_power == 0
