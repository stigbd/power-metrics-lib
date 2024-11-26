"""Unit test module for the calculate_metrics functions."""

from power_metrics_lib.models import Metrics


def test_calculate_average_power() -> None:
    """Test the calculate_average_power function."""
    power_data = [100, 200, 300, 400, 500]
    expected_average_power = 300.0

    metrics = Metrics(power=power_data)

    assert expected_average_power == metrics.average_power


def test_calculate_normalized_power() -> None:
    """Test the calculate_normalized_power function."""
    power_data = [150, 156, 158, 161, 168, 162, 159]
    window_size = 3
    expected_normalized_power = 161.0

    metrics = Metrics()
    metrics.calculate_normalized_power(power_data, window_size)
    assert expected_normalized_power == metrics.normalized_power


def test_calculate_intensity_factor() -> None:
    """Test the calculate_intensity_factor function."""
    normalized_power = 300
    ftp = 200
    expected_intensity_factor = 1.5

    metrics = Metrics()
    metrics.calculate_intensity_factor(normalized_power, ftp)

    assert expected_intensity_factor == metrics.intensity_factor


def test_calculate_training_stress_score() -> None:
    """Test the calculate_training_stress_score function."""
    normalized_power = 300
    ftp = 200
    duration = 3600
    intensity_factor = 1.5
    expected_training_stress_score = 225

    metrics = Metrics()
    metrics.calculate_training_stress_score(
        normalized_power=normalized_power,
        ftp=ftp,
        duration=duration,
        intensity_factor=intensity_factor,
    )

    assert expected_training_stress_score == metrics.training_stress_score


def test_calculate_total_work() -> None:
    """Test the calculate_total_work function."""
    power_data = [100, 200, 300, 400, 500]
    expected_total_work = 1500

    metrics = Metrics(power=power_data)
    assert expected_total_work == metrics.total_work


def test_calculate_duration() -> None:
    """Test the calculate_duration function."""
    timestamps = [1, 2, 3, 4, 5]
    expected_duration = 5

    metrics = Metrics(timestamps=timestamps)
    assert expected_duration == metrics.duration


def test_calculate_max_power() -> None:
    """Test the calculate_max_power function."""
    power_data = [100, 200, 300, 400, 500]
    expected_max_power = 500

    metrics = Metrics(power=power_data)
    assert expected_max_power == metrics.max_power


def test_calculate_normalized_power_when_number_of_power_data_is_lt_window_size() -> (
    None
):
    """Should set normalized-power to 0."""
    power_data = [150, 156, 158]
    window_size = 30

    metrics = Metrics()
    metrics.calculate_normalized_power(power_data, window_size=window_size)

    assert metrics.normalized_power == 0
