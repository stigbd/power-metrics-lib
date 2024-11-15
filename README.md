# A project to cacluate the normalized power and other metrics from a .fit file

This a project implementing a library to calculate the normalized power and other metrics from an activity or workout file.

File formats supported:

- .fit

## Installation

```zsh
% pip install power-metrics-lib
```

## Usage

```python
from power_metrics_lib.file_parsers import parse_fit_activity_file
import power_metrics_lib.calculate_metrics as pm

file_path = "tests/files/file.fit"
# Parse the .fit file:
activity_data: list[dict] = parse_fit_activity_file(file_path)

# Extract the power data from the activity data:
power_data: list[int] = [d["power"] for d in activity_data]

# Calculate the average power:
average_power: float = pm.calculate_average_power(power_data)

# Calculate the normalized power:
normalized_power: float = pm.calculate_normalized_power(power_data)

# Set your FTP:
ftp: int = 300

# Calculate the intensity factor:
intensity_factor: float = pm.calculate_intensity_factor(
     normalized_power=normalized_power,
     ftp=ftp,
     )

# Calculate the duration:
duration: dict[str, int |str ] = pm.calculate_duration(power_data)

# Calculate the training stress score:
training_stress_score: float = pm.calculate_training_stress_score(
     normalized_power=normalized_power,
     intensity_factor=intensity_factor,
     ftp=ftp,
     duration=duration["seconds"],
     )
```
## Install the library into the virtual environment

```zsh
% uv pip install -e .
```
## Notebooks

The project includes a Jupyter notebook to demonstrate how to use the library.

Start the JupyterLab server:

```zsh
% uv run --with jupyter jupyter lab
```

Choose the kernel `power-metrics` to run the notebook.

To install packages in a Jupyter notebook without persisting the change this project, use the following command:

```notebook
!uv pip install matplotlib
```

## References

- [FIT SDK](https://www.thisisant.com/resources/fit/)
- [Cycling Training: Easily Understand Normalized Power in 4 Steps](https://jaylocycling.com/easily-understand-cycling-normalized-power/)
- [Normalized Power](https://www.trainingpeaks.com/blog/normalized-power/)
- [FIT File Viewer](https://www.fitfileviewer.com/)
- [Training tools](https://www.mapmytracks.com/tools/tss-calculator)
- [Zwift Workout Editor](https://www.zwiftworkout.com/)
- [Test file on Strava](https://www.strava.com/activities/12868899187)

- Notebooks:
  - [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
