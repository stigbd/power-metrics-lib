# A project to cacluate the normalized power and other metrics from a .fit file

This a project implementing a library to calculate the normalized power and other metrics from an activity or workout file.

File formats supported:

- .fit
- .zwo

## Introduction

Normalized power can be calculated using the following method:

- Calculate a rolling 30-second average power for the workout or specific section of data
- Raise the resulting values to the fourth power.
- Determine the average of these values.
- Find the fourth root of the resulting average.

## Usage

```zsh
% uv run power-metrics-lib/hello.py
```

## References

- [FIT SDK](https://www.thisisant.com/resources/fit/)
- [Cycling Training: Easily Understand Normalized Power in 4 Steps](https://jaylocycling.com/easily-understand-cycling-normalized-power/)
- [Normalized Power](https://www.trainingpeaks.com/blog/normalized-power/)
- [FIT File Viewer](https://www.fitfileviewer.com/)
- [Training tools](https://www.mapmytracks.com/tools/tss-calculator)
- [Zwift Workout Editor](https://www.zwiftworkout.com/)
- [Test file on Strava](https://www.strava.com/activities/12868899187)
