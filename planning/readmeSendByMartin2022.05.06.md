# Drift-Community-Api (Version 1.4.14)

# Endpoints

Web-Request settings

* **Accept** : `application/json`
* **Content-Type** : `application/json`
* **Time Fields**: `All time values are in coordinate world time standard (Coordinated Universal Time, UTC) and are synchronized between all clients with an inaccuracy of ~0-20ms.`

User in app settings

* **uri** : The uri will be the address where the webservice is located
* **game_id** : The game id for the current race
* **user_name** : A chosen username (not identical with the drift username)

Body Wrapper

```json
{
  "app_version": "1.4.13",
  "game_id": "Race2022",
  "user_id": "b5c5a6e3-3378-4d61-bd3f-02510827d1bf",
  "user_name": "Racer5000",
  "time": "2022-04-22T06:56:09.6986656Z",
  "data": {}
}
```

```
app_version: The current app version, can be used to find changed between the Community Api requests
game_id: The game id for the current race
user_id: Is a generated uid and will be refreshed every time the uri has changed
user_name: A chosen username (not identical with the drift username)
time: This is always and only the send time of the request (do not use this for any game specific content there will be a separate field)
data: Different for each endpoint and will have the actual data  
```

## Ping

**GET** : `<uri>/<game_id>/ping`  
**Body** : `nothing`  
**Response**:

```json
{
  "status": true,
  "start_time": "2022-04-22T06:57:00.0000000Z",
  "lap_count": 5,
  "track_condition": "drift_dirt",
  "track_bundle": "rally",
  "wheels": "spikes",
  "setup_mode": "DRIFT"
}
```

```
status: (required)
If true there is a valid race to join.

start_time: (optional)
If set this time will be used as preset.

The time needs to be in coordinate world time standard (Coordinated Universal Time, UTC)
possible formats are:
    - 2008-06-15T21:15:07.0000000
    - 2008-06-15T21:15:07
    - 2008-06-15 21:15:07Z
    - Sunday, June 15, 2008 9:15 PM
    - Sunday, June 15, 2008 9:15:07 PM
    - 6/15/2008 9:15 PM
    - 6/15/2008 9:15:07 PM

lap_count: (optional / Race only)
If set the amount of laps will be used as preset

track_condition: (optional)
If set this underground will be used as preset

track_bundle: (optional / Race only)
If set this underground bundle will be used as preset

wheels: (optional)
If set this wheels will be set as preset

setup_mode: (optional)
If set this setup will be used as preset
```

## Enter

Will be sent if the user clicks on "start game" inside the app. Use this to let the user join to the race.

**POST** : `<uri>/<game_id>/enter`  
**Body** :

```json
{
  "app_version": "1.4.13",
  "game_id": "Race2022",
  "user_id": "b5c5a6e3-3378-4d61-bd3f-02510827d1bf",
  "user_name": "Racer5000",
  "time": "2022-04-22T06:56:09.6986656Z",
  "data": {
    "game_mode": "RACE",
    "start_time": "2022-04-22T06:57:00.0000000Z",
    "lap_count": 1,
    "track_condition": "drift_dirt",
    "track_bundle": "rally",
    "wheels": "spikes",
    "setup_mode": "DRIFT",
    "engine_type": "V8",
    "tuning_type": "BASIC SETUP 550 PS",
    "steering_angle": 60.0,
    "soft_steering": true,
    "drift_assistant": true
  }
}
```

```json
{
  "game_modes": [
    "RACE",
    "GYMKHANA"
  ],
  "track_conditions": [
    "drift_asphalt",
    "drift_asphalt_wet",
    "drift_dirt",
    "drift_ice",
    "drift_sand"
  ],
  "track_bundles": [
    "none",
    "rally",
    "rally_cross"
  ],
  "wheels": [
    "normal",
    "spikes",
    "gravel_tires"
  ],
  "setup_modes": [
    "RACE",
    "DRIFT"
  ]
}
```

```
All values can be different for each user if no predefined values were sent in the ping response or the user changed them manually.  
game_mode: The game mode that was used for this race 
start_time: The user specific start time.
lap_count: The amount of laps for the race game mode
track_condition: The underground for the race
track_bundle: The underground bundle for each target for the race game mode 
```

**Response**: `nothing`

## Signal Start

Will be sent directly after the start lights.

**POST** : `<uri>/<game_id>/start`  
**Body** :

```json
{
  "app_version": "1.4.13",
  "game_id": "Race2022",
  "user_id": "b5c5a6e3-3378-4d61-bd3f-02510827d1bf",
  "user_name": "Racer5000",
  "time": "2022-04-22T06:57:04.6605584Z",
  "data": {
    "signal_time": "2022-04-22T06:57:04.6605584Z"
  }
}
```

```
signal_time: The actual time if the signal lamp shows the green light.
```

**Response**: `nothing`

## Target

Will be sent differently between game modes. But always if the car-sensor recognizes any target. There are some checks
if the target will be used or not.

**POST** : `<uri>/<game_id>/target`  
**Body** :

```json
{
  "app_version": "1.4.13",
  "game_id": "Race2022",
  "user_id": "b5c5a6e3-3378-4d61-bd3f-02510827d1bf",
  "user_name": "Racer5000",
  "time": "2022-04-22T06:57:22.6539072Z",
  "data": {
    "crossing_time": "2022-04-22T06:57:22.6529069Z",
    "target_code": 0,
    "false_start": false,
    "driven_distance": 180.993896484375,
    "driven_time": 17.968835830688478,
    "score": 0
  }
}
```

```
crossing_time: The time at which the car crossed the target. 
false_start: If a false start was detected this field is always true.
driven_distance: The current driven distance.
driven_time: The current driven time.
score: In race mode it's always 0. In gymkhana mode this will be the score for the actual figure. Due to score calculation for some Gymkhana figures takes some time the response will be sent at a later time.
```

**Response**: `nothing`

## End

Will be sent if the user stops the car. It is not sent directly after the end of the race (crossing the finish line),
because the calculation and validation of the score is done on the results screen.

**POST** : `<uri>/<game_id>/end`  
**Body** :

```json
{
  "app_version": "1.4.13",
  "game_id": "",
  "user_id": "150a31a4-ddd4-459d-8e53-d61cfe544d13",
  "user_name": "",
  "time": "2022-04-22T06:57:36.3928211Z",
  "data": {
    "finished_time": "2022-04-22T06:57:22.6529069Z",
    "false_start": false,
    "total_score": 92,
    "total_driven_distance": 180.993896484375,
    "total_driven_time": 17.968835830688478
  }
}
```

```
finished_time: The time at wich the race ends.
false_start: If a false start was detected this field is true.
total_score: The total score for the race.
total_driven_distance: The total driven distance to the finished_time.
total_driven_time: The total driven time to the finished_time.
```

**Response**: `nothing`

# Target Codes

### Gymkhana

| Code | Description |
| :----: | :-------- |
| 0 | Start / Finish |
| 4 | Speed Drift |
| 5 | Angle Drift |
| 6 | 180 |
| 7 | 360 |

### Race

| Code | RACE | RACE (Rally) | Race (Rally Cross) |
| :----: | :---- | :------------ | :------------------ |
| 0 | Start / Finish | Start / Finish | Start / Finish |
| 4 |  | drift_asphalt | drift_asphalt |
| 5 |  | drift_asphalt_wet | drift_asphalt_wet |
| 6 |  | drift_dirt | drift_dirt |
| 7 |  | drift_ice | drift_sand |