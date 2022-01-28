# Smart Bed

See working prototype at [www.zack.land](https://www.zack.land/portfolio/misc#Smart-Bed)

This app is running on a RaspberryPi 3 B+. 
There are 5 independent RGBWWCW LED strips to set multiple lighting configurations. 
There are 4 load cells (2 for each side of the bed) that dectect user presence. 
There are rocker switches on each side of the bed to toggle built in night lamps.

## Installation

### Open Lighting Project

OLA installation instructions for Ubuntu [here](http://opendmx.net/index.php/OLA_Debian_/_Ubuntu)

OLA is not python 3 compatable, so in order to install what is needed, run:

```
python3 -m pip install
```

in main directory, create a file called `status.json`.

Also in main directory, create a file called `environment.py`, and fill out the following fields:
```
import os

os.environ['DEVICE_ROOM'] = 'Your Bedroom name'

# for sun tracking
os.environ['DEVICE_LATITUDE'] = ''
os.environ['DEVICE_LONGITUDE'] = ''

# pin mapping of the 4 load cells
os.environ['LOAD_CELL_LEFT_DT'] = ''
os.environ['LOAD_CELL_LEFT_SCK'] = ''
os.environ['LOAD_CELL_RIGHT_DT'] = ''
os.environ['LOAD_CELL_RIGHT_SCK'] = ''

# pin mapping of the rocker switches
os.environ['ROCKER_LEFT_UP'] = ''
os.environ['ROCKER_LEFT_DOWN'] = ''
os.environ['ROCKER_RIGHT_UP'] = ''
os.environ['ROCKER_RIGHT_DOWN'] = ''

os.environ['API_PORT'] = '8080'

os.environ['HOME_AUTOMATION_URL'] = ''
```

## Start App

to start the app run:
```
nohup python3 -m smart_bed &
```

You can now open `status.json` and be able to see all the data that the bed tracks:

```
{
    "room": "Your Room Name",
    "is_occupied_left": false,
    "time_last_occupied_left": null,
    "is_occupied_right": false,
    "time_last_occupied_right": null,
    "context": "night",
    "time_lamp_on_left": null,
    "time_lamp_on_right": null,
    "is_fun_mode": false,
    "volume_change": 0
}
```

## End App

to end the app, first get the pid by running:
```
ps -ef |grep smart_bed
```
then end it:
```
kill <pid> 
```