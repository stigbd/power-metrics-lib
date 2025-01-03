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
from power_metrics_lib import Activity

# Set your FTP:
ftp: int = 300
# Create an activity from the .fit file:
file_path = "tests/files/activity.fit"

# Create an activity object:
activity = Activity(file_path=file_path, ftp=ftp)

# Investigate the metrics:
print(activity.average_power)
print(activity.normalized_power)
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

- Power profiling:
  - [Creating Your Power Profile](https://www.trainingpeaks.com/blog/power-profiling/)
  - [Cycling Power Profiling Explained](https://www.highnorth.co.uk/articles/power-profiling-cycling)

- Notebooks:
  - [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/)
