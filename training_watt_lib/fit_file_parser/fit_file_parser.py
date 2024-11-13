"""Module for parsing .fit files."""

from garmin_fit_sdk import Decoder, Stream


def parse_fit_file(file_path: str) -> list[dict[str, str | int | float | bytes]]:
    """Parse a .fit file and return a list of dicts."""
    stream = Stream.from_file(file_path)
    decoder = Decoder(stream)
    messages, errors = decoder.read(
        convert_datetimes_to_dates=False,
        convert_types_to_strings=True,
    )
    if len(errors) > 0:  # pragma: no cover
        msg = "\n".join(errors)
        raise ValueError(msg)

    return messages["record_mesgs"]
