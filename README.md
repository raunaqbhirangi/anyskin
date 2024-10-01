# AnySkin Sensor Library
This is a python library to interface with [AnySkin](https://any-skin.github.io) sensors. Much of this is adapted and streamlined from the [reskin_sensor](https://github.com/raunaqbhirangi/reskin_sensor) library. We provide two classes for interfacing with [AnySkin](https://openreview.net/forum?id=87_OJU4sw3V). The `AnySkinBase` class is good for standalone data collection: it blocks code execution while data is being collected. The `AnySkinProcess` class can be used for non-blocking background data collection. Data can be buffered in the background while you run the rest of your code.

Latest stable release is v1.0.0

## Installation

This package can be installed using pip:
```
pip install anyskin
```
Alternatively, if you would like the latest (potentially unstable) version,
1. Clone this repository using
```
$ git clone https://github.com/raunaqbhirangi/anyskin.git --recursive
```
2. Install this package using
```
$ pip install -e .
```

## Usage: Quick Setup
This guide assumes you are using the AnySkin startup kit.

1. Connect the magnetometer circuit board to the microcontroller using the provided QWIIC cable.

2. Insert the circuit board into the fingertip slot and pull the skin over the printed 3D tip.

3. Connect the microcontroller (Adafruit QT Py) to your computer using a USB-C cable.

4. Find the dev path your microcontroller is connected to. The simplest way to do this is:
<br><br>Linux: `ls /dev/ | grep -e ACM -e USB`
<br>MacOS: `ls /dev/ | grep cu.usb`
<br>Windows: `TODO`
<br><br>If you have no other devices connected, this should give you a single path. If you see multiple, disconnect the microcontroller and run the command again. Reconnect the microcontroller and re-run the command. The additional path is your `device-port`

5. Run the visualizer with the port identified in the previous step: <br>`python visualizations/anyskin_viz.py -p device-port`

## Usage: Full Setup
This guide is recommended if you are relatively familiar with AnySkin and are using independently sourced components.

1. Connect the magnetometer circuit board to the microcontroller.

2. Connect the microcontroller (we recommend the Adafruit Trinket M0 or the Adafruit QT PY) to the computer using a suitable USB cable

3. Use the [Arduino IDE](https://www.arduino.cc/en/software) to upload code to a microcontroller. The code as well as upload instructions can be found in the [arduino](./arduino) folder.
If you get a `can't open device "<port-name>": Permission denied` error, modify permissions to allow read and write on that port. On Linux, this would look like
```
$ sudo chmod a+rw <port-name>
```

4. Run test code on the computer
```
$ python tests/sensor_proc_test.py -p <port-name>
```
## Credits
This package is maintained by [Raunaq Bhirangi](https://www.cs.cmu.edu/~rbhirang/). We would also like to cite the [pyForceDAQ](https://github.com/lindemann09/pyForceDAQ) library which was used as a reference in structuring this package.
