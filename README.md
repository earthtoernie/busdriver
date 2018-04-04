## busdriver
... it two things
1. a collection of python scripts to talk to embedded devices like
_real time clocks_ , _temperature and humidity sensors_ , _graphic lcd displays_
2. libraries to work with the mentioned devices

#### why I wrote this
* would rather prototype using a desktop instead of raspi or arduino board
* havent found an easy to use python library that is easy to use and covers *many* different devices
* use this to prototype and develop *perminent* embedded projects
* learn how to write clean *modular* python code

### future dev goals
* make comparable with Adafruit-GFX-Library
* adapt to work with raspi gpio suport *or* bus pirate

### supported devices (stuff that I have lying around )
* real time clock DS3231 DS1307
* graphic lcd st7565 126 x 64 (in progress)
* SHARP memory lcd  1.26" 144x168 LS013B7DH05 (planned)
* SHARP memory lcd  2.7" 400 × 240 LS027B7DH01A (planned)
* Sensiron SHT31 Temperature & Humidity Sensor (planned)


__creating a virtual environment__
or just install, only dependency is 'pyserial' and shell scripts are installed with the name 'bp_*'
tested with python3 on linux

1. if have a venv that is messed up, run `deactivate` then delete `venv` folder.
3. create the virtual environment in a folder called `venv`
`python3 -m venv venv`
4. `source venv/bin/activate`
5. `pip install --upgrade setuptools` always run this to update setuptools local to the venv
6. `pip install -e .`


__getting statted__ , an example
* try to get and set time from DS3231 *
* acquire a bus pirate , tested on v3.6 and v4
* acquire a breakout board. I used a "ZS-042 Real-time Clock Module" which costs about $4 
* connect bus pirate to usb and DS3231
* `bp_dallas get` returns `Sat Mar 31 20:03:25 XXX 2018`

attach a bus pirate
**get time**

sites that I referenced
https://edeca.net/pages/the-st7565-display-controller/