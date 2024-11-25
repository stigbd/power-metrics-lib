"""Module for converting workout data to activity data."""

from power_metrics_lib.models import (
    Activity,
    Cooldown,
    FreeRide,
    Interval,
    Ramp,
    SteadyState,
    Warmup,
    Workout,
)


def transform_workout_to_activity(workout: Workout, ftp: int) -> Activity:  # noqa: C901
    """Converts a workout to an activity.

    Args:
        workout: The workout data.
        ftp: The functional threshold power.

    Returns:
        Activity: The workout as an activity.

    Raises:
        TypeError: If the block type is invalid.
    """
    activity = Activity()
    timestamp = 1
    for block in workout.blocks:
        if isinstance(block, Warmup | Cooldown | Ramp):
            # Calculate the power increase per second
            power_increase_per_second = (
                block.end_power - block.start_power
            ) / block.duration
            for i in range(block.duration):
                activity.timestamps.append(timestamp)
                power = block.start_power + i * power_increase_per_second
                activity.power.append(round(power * ftp if power > 0 else 0))
                timestamp += 1
        elif isinstance(block, SteadyState):
            for _ in range(block.duration):
                activity.timestamps.append(timestamp)
                activity.power.append(round(block.power * ftp))
                timestamp += 1
        elif isinstance(block, Interval):
            for _ in range(block.repeat):
                for _ in range(block.on_duration):
                    activity.timestamps.append(timestamp)
                    activity.power.append(round(block.on_power * ftp))
                    timestamp += 1
                for _ in range(block.off_duration):
                    activity.timestamps.append(timestamp)
                    activity.power.append(round(block.off_power * ftp))
                    timestamp += 1
        elif isinstance(block, FreeRide):
            pass
        else:
            msg = f"Invalid block type: {type(block)}"
            raise TypeError(msg) from None
    return activity
