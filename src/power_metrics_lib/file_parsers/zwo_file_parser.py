"""This module contains functions for parsing .zwo files."""

from defusedxml.ElementTree import parse


def parse_zwo_workout_file(file_path: str) -> list[dict[str, str | int | float]]:
    """Parse a .zwo file and return a list of dicts.

    Args:
        file_path (str): The path to the .zwo file.

    Returns:
        list[dict[str, str | int | float]]: A list of dicts containing the parsed data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If there are any errors parsing the .zwo file.

    Examples:
        >>> from power_metrics_lib.file_parsers import parse_zwo_workout_file
        >>> zwo_file = "tests/files/zwift_workout.zwo"
        >>> # Parse the .zwo file:
        >>> workout_data: list[dict] = parse_zwo_workout_file(zwo_file)
    """
    try:
        tree = parse(file_path)
    except FileNotFoundError as e:
        msg = f"File not found: {file_path}"
        raise FileNotFoundError(msg) from e

    root = tree.getroot()
    steps_in_workout = root.findall("./workout/*")

    steps = []
    for step in steps_in_workout:
        if step.tag == "SteadyState":
            power = float(step.attrib["Power"])
            duration = float(step.attrib["Duration"])
            steps.append({"step_type": step.tag, "power": power, "duration": duration})
        elif step.tag in ("Cooldown", "Warmup", "Ramp"):
            power_low = float(step.attrib["PowerLow"])
            power_high = float(step.attrib["PowerHigh"])
            duration = float(step.attrib["Duration"])
            steps.append(
                {
                    "step_type": step.tag,
                    "duration": duration,
                    "power_low": power_low,
                    "power_high": power_high,
                }
            )
        elif step.tag == "IntervalsT":
            repeat = int(step.attrib["Repeat"])
            on_power = float(step.attrib["OnPower"])
            off_power = float(step.attrib["OffPower"])
            on_duration = float(step.attrib["OnDuration"])
            off_duration = float(step.attrib["OffDuration"])
            steps.append(
                {
                    "step_type": step.tag,
                    "repeat": repeat,
                    "on_duration": on_duration,
                    "on_power": on_power,
                    "off_duration": off_duration,
                    "off_power": off_power,
                }
            )
        elif step.tag == "FreeRide":
            duration = float(step.attrib["Duration"])
            steps.append({"step_type": step.tag, "duration": duration})
        else:
            msg = f"Unknown step type: {step.tag}"
            raise ValueError(msg) from None

    return steps
