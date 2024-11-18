# Workouts

## Zwift Workout format (.zwo)

Zwift workouts are stored in a custom XML format with the `.zwo` file extension.

### Block types

#### `Warmup`

A [`Ramp`](#ramp) block put at the end of a workout where the power target will _increase_ linearly from `PowerLow` to `PowerHigh` over the duration of the block.

| Property  | Type    | Example | Description                               |
| --------- | ------- | ------- | ----------------------------------------- |
| Duration  | int     | 600     | Duration of the block in seconds          |
| PowerLow  | float   | 0.25    | Lower bound of the power target in % of FTP |
| PowerHigh | float   | 0.75    | Upper bound of the power target in % of FTP |

#### `FreeRide`

A block without a power target.
(Will be ignored by when tranforming to an activity file.)

| Property | Type    | Example | Description |
| -------- | ------- | ------- | ----------- |
| Duration | int     | 600 | Duration of the block in seconds |


#### `SteadyState`

A block with a constant power target.

| Property  | Type    | Example | Description                               |
| --------- | ------- | ------- | ----------------------------------------- |
| Duration  | int     | 600     | Duration of the block in seconds          |
| Power     | float   | 0.50    | Power the power target in % of FTP |

#### `IntervalsT`

A block with a work and rest period repeated a number of times.

| Property    | Type    | Example | Description                               |
| ----------- | ------- | ------- | ----------------------------------------- |
| Repeat      | int     | 5       | Number of times to repeat the interval    |
| OnDuration  | int     | 40      | Duration of the work period in seconds    |
| OffDuration | int     | 20      | Duration of the rest period in seconds    |
| OnPower     | float   | 0.80    | Power target of the work part in % of FTP |
| OffPower    | float   | 0.50    | Power target of the rest part in % of FTP |

#### `Ramp`

Power target will increase or decrease linearly from `PowerLow` to `PowerHigh` over the duration of the block.

| Property  | Type    | Example | Description                               |
| --------- | ------- | ------- | ----------------------------------------- |
| Duration  | int     | 600     | Duration of the block in seconds          |
| PowerLow  | float   | 0.25    | Lower bound of the power zone in % of FTP |
| PowerHigh | float   | 0.75    | Upper bound of the power zone in % of FTP |

#### `Cooldown`

A `Ramp` block put at the end of a workout where the power target will _decrease_ linearly from `PowerLow` to `PowerHigh` over the duration of the block.

| Property  | Type    | Example | Description                               |
| --------- | ------- | ------- | ----------------------------------------- |
| Duration  | seconds | 600     | Duration of the block in seconds          |
| PowerLow  | float   | 0.25    | Lower bound of the power zone in % of FTP |
| PowerHigh | float   | 0.75    | Upper bound of the power zone in % of FTP |
