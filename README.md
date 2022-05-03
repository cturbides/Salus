# Salus
## _Automate hospital monitoring_

Salus is a web project that enable monitoring the whole Hospital
via web. Nurses and operators can benefit from this project, using
the software to see through all the hospital rooms without to
manually enter them.
With Salus you can visualize in real time:
- Patient pulse
- Patient's temperature
- Patient's muscle state 
- Patient's room air quality
- Patient's room temperature
- Patient's room relative humidity
- And so on.

## Dependencies

To work, Salus uses:
- [Django] - All project backend
- [Django channels] - Real time websockets
- [Redis Server] - To store data in memory
- [Arduino] - Where all sensor data is collected
- [Raspberry] - The central core of the project
- [Chart.js] - Display beautiful purple charts in real time

## Installation

Salus requires [Python 3](https://www.python.org/) to run.

Install the dependencies: 

```sh
python3 pip install django channels channels-redis pyserial
```

To install redis:
In arch: 
 ```sh
sudo pacman -S redis
```
With apt:
```sh
sudo apt install redis-server
```
### Setting up your arduino
You will need some sensors, such as:
- MQ-135 -> A0
- PulseSensor -> A5 
- DHT-11 -> D2
- DustSensor -> A2
- Electromiography (homemade) -> A1

Change line 12 of [salusArduino.ino] according to your model:
```c++
#define placa "Arduino MEGA" 
```
Upload to your Arduino.
Next change the line 6 and 7 of [Wrapper.py] file:
```py
BOARD = 'Arduino MEGA'
PORT = '/dev/ttyACM0'
```
After that, run [Wrapper.py] indicating a room id, for example :
```sh
python3 Wrapper.py 1
```

#### Starting the server

From Salus core dir:
```sh
cd SalusWeb
redis-server &
python3 manage.py runserver 0.0.0.0:8000
```
Now just enter into [salusApp] 

> Note: You have to create an account to get into the system.


## Captures

![Home view](./screenshots/main.png?raw=true)
![My Hospital](./screenshots/mi-clinica.png?raw=true)
![Patient graphs](./screenshots/patient-graph.png?raw=true)

## License
[MIT]

[//]: #
   [Django]: <https://www.djangoproject.com/>
   [Redis Server]: <https://redis.io/>
   [Arduino]: <https://www.arduino.cc/>
   [Raspberry]: <https://www.raspberrypi.org/>
   [Django channels]: <https://channels.readthedocs.io/en/stable/>
   [Wrapper.py]: <./Wrapper.py>
   [salusArduino.ino]: <./Arduino/salusArduino/salusArduino.ino>
   [Chart.js]: <https://chartjs.org/>
   [salusApp]: <localhost:8000/salusApp/>
   [MIT]: <./LICENSE>
