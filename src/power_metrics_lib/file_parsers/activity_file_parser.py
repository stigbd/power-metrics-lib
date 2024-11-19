"""Module for parsing activity files."""

from garmin_fit_sdk import Decoder, Stream

from power_metrics_lib.models import Activity


def parse_activity_file(file_path: str) -> Activity:
    """Parse a .fit file and return a list of dicts.

    Args:
        file_path (str): The path to the .fit file.

    Returns:
        An activity object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If there are any errors parsing the .fit file.

    Examples:
        >>> from power_metrics_lib.file_parsers import parse_activity_file
        >>> # Parse the .fit file:
        >>> activity: Activity = parse_activity_file("tests/files/file.fit")
        >>>
        >>> # Get the power data from the activity object:
        >>> power_data: list[int] = activity.power
    """
    try:
        stream = Stream.from_file(file_path)
    except FileNotFoundError as e:
        msg = f"File not found: {file_path}"
        raise FileNotFoundError(msg) from e

    decoder = Decoder(stream)
    messages, errors = decoder.read(
        convert_datetimes_to_dates=False,
        convert_types_to_strings=True,
    )

    if len(errors) > 0:  # pragma: no cover
        msg = "\n".join(errors)
        raise ValueError(msg) from None

    if "record_mesgs" not in messages:
        msg = "No record messages found in the .fit file."
        raise ValueError(msg) from None

    return Activity(
        timestamps=[m["timestamp"] for m in messages["record_mesgs"]],
        power=[m["power"] for m in messages["record_mesgs"]],
    )
