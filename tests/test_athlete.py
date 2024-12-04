"""Tests for the Athlete class."""

from power_metrics_lib import Athlete


def test_create_athlete() -> None:
    """Should return a new Athlete object with w_pr_kg."""
    athlete = Athlete(name="Alice")

    assert athlete.name == "Alice"
    assert athlete.uuid is not None
    assert athlete.get_ftp() is None
    assert athlete.get_weight() is None
    assert athlete.get_ftp_pr_kg() is None


def test_create_athlete_with_weight_and_ftp() -> None:
    """Should return a new Athlete object with w_pr_kg."""
    expected_ftp = 200
    expected_weight = 70

    athlete = Athlete(name="Alice", ftp=expected_ftp, weight=expected_weight)

    athlete.set_ftp(ftp=expected_ftp)

    assert athlete.name == "Alice"
    assert athlete.uuid is not None
    assert expected_ftp == athlete.get_ftp()
    assert expected_weight == athlete.get_weight()


def test_create_athlete_with_dated_weight_and_ftp() -> None:
    """Should return a new Athlete object with w_pr_kg."""
    expected_ftp = 200

    athlete = Athlete(name="Alice")

    athlete.set_ftp(ftp=expected_ftp, from_date="2021-01-01")

    assert athlete.name == "Alice"
    assert athlete.uuid is not None
    assert expected_ftp == athlete.get_ftp(from_date="2021-01-01")


def test_get_ftp_for_date_earlier_than_existing_ftps() -> None:
    """Should return None."""
    expected_ftp = None

    athlete = Athlete(name="Alice")

    athlete.set_ftp(ftp=200, from_date="2021-01-02")

    assert athlete.get_ftp(from_date="2021-01-01") == expected_ftp


def test_get_all_ftps() -> None:
    """Should return sorted list of all FTPs and dates."""
    # Expected FTPs and dates in descending order:
    exptected_ftps = [("2021-01-02", 210), ("2021-01-01", 200)]

    athlete = Athlete(name="Alice")

    # If no ftp is set, return None:
    assert athlete.get_all_ftps() is None

    # Set the FTP for specific dates:
    athlete.set_ftp(ftp=200, from_date="2021-01-01")
    athlete.set_ftp(ftp=210, from_date="2021-01-02")

    # Get all FTPs and their dates:
    assert athlete.get_all_ftps() == exptected_ftps


def test_get_weight_for_date_later_than_existing_weights() -> None:
    """Should return the correct weight."""
    expected_weight = 75

    athlete = Athlete(name="Alice")

    athlete.set_weight(weight=70, from_date="2021-01-01")
    athlete.set_weight(weight=75, from_date="2021-01-02")

    assert athlete.get_weight(from_date="2021-01-02") == expected_weight


def test_get_weight_for_date_earlier_than_existing_weights() -> None:
    """Should return None."""
    expected_weight = None

    athlete = Athlete(name="Alice")

    athlete.set_weight(weight=70, from_date="2021-01-02")

    assert athlete.get_weight(from_date="2021-01-01") == expected_weight


def test_get_all_weights() -> None:
    """Should return sorted list of all weights and dates."""
    # Expected weights and dates in descending order:
    exptected_weights = [("2021-01-02", 75), ("2021-01-01", 70)]

    athlete = Athlete(name="Alice")

    # If no weight is set, return None:
    assert athlete.get_all_weights() is None

    # Set the weight for specific dates:
    athlete.set_weight(weight=70, from_date="2021-01-01")
    athlete.set_weight(weight=75, from_date="2021-01-02")

    # Get all weights and their dates:
    assert athlete.get_all_weights() == exptected_weights


def test_get_ftp_pr_kg() -> None:
    """Should return the correct weight per kg."""
    weight = 75
    ftp = 225
    expected_ftp_pr_kg = weight / ftp

    athlete = Athlete(name="Alice")

    athlete.set_weight(weight=weight, from_date="2021-01-01")
    athlete.set_ftp(ftp=ftp, from_date="2021-01-02")

    assert athlete.get_ftp_pr_kg(from_date="2021-01-02") == expected_ftp_pr_kg


def test_get_all_ftp_pr_kg() -> None:
    """Should return sorted list of all weights per kg and dates."""
    # Expected weights per kg and dates in descending order,
    # which is a merge of ftps and weights:
    weights = [("2021-01-01", 75), ("2021-03-01", 70)]
    ftps = [("2021-01-01", 200), ("2021-02-01", 225), ("2021-03-01", 250)]
    exptected_ftp_pr_kg = [
        ("2021-03-01", 250 / 70),
        ("2021-02-01", 225 / 75),
        ("2021-01-01", 200 / 75),
    ]

    athlete = Athlete(name="Alice")

    # If no weight or ftp is set, return None:
    assert athlete.get_all_ftp_pr_kg() is None

    # Set the weight and ftp for specific dates:
    athlete.set_weight(from_date=weights[0][0], weight=weights[0][1])
    athlete.set_weight(from_date=weights[1][0], weight=weights[1][1])
    athlete.set_ftp(from_date=ftps[0][0], ftp=ftps[0][1])
    athlete.set_ftp(from_date=ftps[1][0], ftp=ftps[1][1])
    athlete.set_ftp(from_date=ftps[2][0], ftp=ftps[2][1])

    # Get all weights per kg and their dates
    all_ftp_pr_kgs = athlete.get_all_ftp_pr_kg()

    assert all_ftp_pr_kgs is not None
    assert len(all_ftp_pr_kgs) == len(exptected_ftp_pr_kg)
    assert all_ftp_pr_kgs == exptected_ftp_pr_kg
