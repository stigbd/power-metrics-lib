# Reference

::: power_metrics_lib.file_parsers
    options:
      members:
       - parse_activity_file

::: power_metrics_lib.calculate_metrics
    options:
      members:
       - calculate_average_power
       - calculate_normalized_power
       - calculate_intensity_factor
       - calculate_duration
       - calculate_training_stress_score
       - calculate_total_work
       - calculate_max_power

::: power_metrics_lib.models
    options:
      include-members: true
      show-inheritance: true

::: power_metrics_lib.transformers
    options:
      members:
       - transform_workout_to_activity
