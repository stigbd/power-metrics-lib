"""Module for parsing workout files."""

from defusedxml.ElementTree import parse


def parse_workout_file(file_path: str) -> list[dict]:
    """Parse a .zwo file and return a workout object.

    Args:
        file_path (str): The path to the .zwo file.

    Returns:
        Workout: the workout object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If there are any errors parsing the .zwo file.

    Examples:
        >>> from power_metrics_lib.file_parsers import parse_workout_file
        >>> zwo_file = "tests/files/zwift_workout.zwo"
        >>> # Parse the .zwo file:
        >>> workout_data: list[dict] = parse_workout_file(zwo_file)
    """
    try:
        tree = parse(file_path)
    except FileNotFoundError as e:
        msg = f"File not found: {file_path}"
        raise FileNotFoundError(msg) from e

    root = tree.getroot()
    blocks_in_workout = root.findall("./workout/*")

    blocks = []
    for block in blocks_in_workout:
        if block.tag == "SteadyState":
            power = float(block.attrib["Power"])
            duration = int(round(float(block.attrib["Duration"])))
            blocks.append({"SteadyState": {"power": power, "duration": duration}})
        elif block.tag in ("Cooldown", "Warmup", "Ramp"):
            power_low = float(block.attrib["PowerLow"])
            power_high = float(block.attrib["PowerHigh"])
            duration = int(round(float(block.attrib["Duration"])))
            if block.tag == "Cooldown":
                blocks.append(
                    {
                        "Cooldown": {
                            "start_power": power_low,
                            "end_power": power_high,
                            "duration": duration,
                        }
                    }
                )
            elif block.tag == "Warmup":
                blocks.append(
                    {
                        "Warmup": {
                            "start_power": power_low,
                            "end_power": power_high,
                            "duration": duration,
                        }
                    }
                )
            else:
                # "Ramp"
                blocks.append(
                    {
                        "Ramp": {
                            "start_power": power_low,
                            "end_power": power_high,
                            "duration": duration,
                        }
                    }
                )
        elif block.tag == "IntervalsT":
            repeat = int(block.attrib["Repeat"])
            on_power = float(block.attrib["OnPower"])
            off_power = float(block.attrib["OffPower"])
            on_duration = int(round(float(block.attrib["OnDuration"])))
            off_duration = int(round(float(block.attrib["OffDuration"])))

            blocks.append(
                {
                    "Interval": {
                        "repeat": repeat,
                        "on_power": on_power,
                        "off_power": off_power,
                        "on_duration": on_duration,
                        "off_duration": off_duration,
                    }
                }
            )
        elif block.tag == "FreeRide":
            duration = int(round(float(block.attrib["Duration"])))
            blocks.append({"FreeRide": {"duration": duration}})
        else:
            msg = f"Unknown block type: {block.tag}"
            raise ValueError(msg) from None

    return blocks
