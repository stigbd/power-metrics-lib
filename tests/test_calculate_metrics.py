"""Test module the calculate_metrics.py module."""


def test_calculate_average_power() -> None:
    """Test the calculate_average_power function."""
    from power_metrics_lib.calculate_metrics import calculate_average_power

    power_data = [100, 200, 300, 400, 500]
    expected_result = 300.0

    assert calculate_average_power(power_data) == expected_result


def test_calculate_normalized_power() -> None:
    """Test the calculate_normalized_power function."""
    from power_metrics_lib.calculate_metrics import calculate_normalized_power

    power_data = [150, 156, 158, 161, 168, 162, 159]
    window_size = 3
    expected_result = 161.0

    assert (
        calculate_normalized_power(power_data, window_size=window_size)
        == expected_result
    )


def test_calculate_intensity_factor() -> None:
    """Test the calculate_intensity_factor function."""
    from power_metrics_lib.calculate_metrics import calculate_intensity_factor

    normalized_power = 300
    ftp = 200
    expected_result = 1.5

    assert calculate_intensity_factor(normalized_power, ftp) == expected_result


def test_calculate_training_stress_score() -> None:
    """Test the calculate_training_stress_score function."""
    from power_metrics_lib.calculate_metrics import calculate_training_stress_score

    normalized_power = 300
    ftp = 200
    duration = 3600
    intensity_factor = 1.5
    expected_result = 225

    assert (
        calculate_training_stress_score(
            normalized_power=normalized_power,
            ftp=ftp,
            duration=duration,
            intensity_factor=intensity_factor,
        )
        == expected_result
    )


def test_calculate_total_work() -> None:
    """Test the calculate_total_work function."""
    from power_metrics_lib.calculate_metrics import calculate_total_work

    power_data = [100, 200, 300, 400, 500]
    expected_result = 1500

    assert calculate_total_work(power_data) == expected_result


def test_calculate_duration() -> None:
    """Test the calculate_duration function."""
    from power_metrics_lib.calculate_metrics import calculate_duration

    power_data = [100, 200, 300, 400, 500]
    expected_result = {"seconds": 5, "hh:mm:ss": "0:00:05"}

    assert calculate_duration(power_data) == expected_result


def test_calculate_max_power() -> None:
    """Test the calculate_max_power function."""
    from power_metrics_lib.calculate_metrics import calculate_max_power

    power_data = [100, 200, 300, 400, 500]
    expected_result = 500

    assert calculate_max_power(power_data) == expected_result
