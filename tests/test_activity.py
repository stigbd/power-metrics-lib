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

    activity = Activity(file_path="tests/files/file.fit", ftp=ftp)

    assert isinstance(activity, Activity)

    # Check that the first record has the expected values:
    assert expected_timestamp_first_record == activity.timestamps[0]
    assert expected_power_first_record == activity.power[0]

    # Check that all the metrics are generated correctly
    assert expected_duration == activity.metrics.duration
    assert expected_avgerage_power == activity.metrics.average_power
    assert expected_normalized_power == activity.metrics.normalized_power
    assert expected_max_power == activity.metrics.max_power
    assert expected_intensity_factor == activity.metrics.intensity_factor
    assert expected_training_stress_score == activity.metrics.training_stress_score
    assert expected_total_work == activity.metrics.total_work


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
