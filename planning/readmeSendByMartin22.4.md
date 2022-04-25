# Drift-Community-Api (Version 1.4.13)

# Endpoints

Web-Request settings

* **Accept** : `application/json`
* **Content-Type** : `application/json`

User in app settings

* **uri** : The uri will be the address where the webservice is located
* **game_id** : The game id for the current race
* **user_name** : A chosen username (not identical with the drift username)
* **user_id** : Is a generated uid and will be refreshed every time the uri has changed

## Ping

**GET** : `<uri>/<game_id>/ping`  
**Body** : `nothing`  
**Response**:

```json
{
  "status": true,
  "start_time": "2022-04-22T06:57:00.0000000Z"
}
```

```
start_time: (optional)
If set this time will be used to predefine the start time inside the app.

The time needs to be in coordinate world time standard (Coordinated Universal Time, UTC)
possible formats are:
    - 2008-06-15T21:15:07.0000000
    - 2008-06-15T21:15:07
    - 2008-06-15 21:15:07Z
    - Sunday, June 15, 2008 9:15 PM
    - Sunday, June 15, 2008 9:15:07 PM
    - 6/15/2008 9:15 PM
    - 6/15/2008 9:15:07 PM
```

## Enter

Will be sent if the user clicks on "start game" inside the app.

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
    "time_limit": 0.0,
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
    "time": "2022-04-22T06:57:22.6529069Z",
    "target_code": 0,
    "false_start": false,
    "driven_distance": 180.993896484375,
    "driven_time": 17.968835830688478,
    "score": 0
  }
}
```

```
score: in gymkhana mode this will be the score for the actual figure. In race mode it's always 0.
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
    "total_score": 92,
    "false_start": false,
    "driven_distance": 180.993896484375,
    "driven_time": 17.968835830688478
  }
}
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
