"""Test module the calculate_metrics.py module."""


def test_calculate_average_power() -> None:
    """Test the calculate_average_power function."""
    from training_watt_lib.calculate_metrics import calculate_average_power

    power_data = [100, 200, 300, 400, 500]
    expected_result = 300.0

    assert calculate_average_power(power_data) == expected_result


def test_calculate_normalised_power() -> None:
    """Test the calculate_normalised_power function."""
    from training_watt_lib.calculate_metrics import calculate_normalised_power

    power_data = [150, 156, 158, 161, 168, 162, 159]
    window_size = 3
    expected_result = 161.0

    assert (
        calculate_normalised_power(power_data, window_size=window_size)
        == expected_result
    )


def test_calcuate_intensity_factor() -> None:
    """Test the calcuate_intensity_factor function."""
    from training_watt_lib.calculate_metrics import calcuate_intensity_factor

    normalised_power = 300
    ftp = 200
    expected_result = 1.5

    assert calcuate_intensity_factor(normalised_power, ftp) == expected_result


def test_calculate_training_stress_score() -> None:
    """Test the calculate_training_stress_score function."""
    from training_watt_lib.calculate_metrics import calculate_training_stress_score

    normalised_power = 300
    ftp = 200
    duration = 3600
    expected_result = 225

    assert (
        calculate_training_stress_score(normalised_power, ftp, duration)
        == expected_result
    )


def test_calcuate_total_work() -> None:
    """Test the calcuate_total_work function."""
    from training_watt_lib.calculate_metrics import calcuate_total_work

    power_data = [100, 200, 300, 400, 500]
    expected_result = 1500

    assert calcuate_total_work(power_data) == expected_result
