# AnySkin Sensor Library
This is a python library to interface with [AnySkin](https://any-skin.github.io) sensors. Much of this is adapted and streamlined from the [reskin_sensor](https://github.com/raunaqbhirangi/reskin_sensor) library. We provide two classes for interfacing with [AnySkin](https://openreview.net/forum?id=87_OJU4sw3V). The `AnySkinBase` class is good for standalone data collection: it blocks code execution while data is being collected. The `AnySkinProcess` class can be used for non-blocking background data collection. Data can be buffered in the background while you run the rest of your code.

Latest stable release is v1.0.0

## Installation

This package can be installed using pip:
```
pip install anyskin
```
Alternatively, if you would like the latest (potentially unstable) version,
1. Clone this repository:
```
git clone https://github.com/raunaqbhirangi/anyskin.git --recursive
```
2. Install this package:
```
pip install -e .
```

## Usage: Quick Setup
This guide assumes you are using the AnySkin startup kit.

1. Connect the magnetometer circuit board to the microcontroller using the provided QWIIC cable.

2. Insert the circuit board into the fingertip slot and pull the skin over the printed 3D tip.

3. Connect the microcontroller (Adafruit QT Py) to your computer using a USB-C cable. The startup kit comes with pre-loaded arduino code. If you would like to change the uploaded code, refer to the [arduino](./arduino) folder.

4. Find the dev path/COM port your microcontroller is connected to. The simplest way to do this is:
<br><br> <b>Linux:</b> `ls /dev/ | grep -e ACM -e USB`. This is generally `/dev/ttyACM0` or `/dev/ttyUSB0`. <br>If you get a `can't open device "<port>": Permission denied` error, modify permissions to allow read and write on that port: `sudo chmod a+rw <port>`
<br> <b>MacOS:</b> `ls /dev/ | grep cu.usb`. This is generally `cu.usbmodem*`.
<br> <b>Windows:</b> Open Device Manager. Click `View` and select `Show Hidden Devices`. Locate `Ports (COM & LPT)`. Note the `COM` port corresponding to the QT Py.
<br><br>If you have no other devices connected, this should give you a single path. If you see multiple, disconnect the microcontroller and run the command again. Reconnect the microcontroller and re-run the command. The additional path is your `<port>`.

5. Run the visualizer with the `<port>` identified in the previous step: <br>`anyskin_viz <port>`

6. Over time, the sensor measurement will drift and you may see a non-zero measurement without any load being applied. When this happens, press the `B` key to recalibrate your zero measurement.

## Credits
This package is maintained by [Raunaq Bhirangi](https://www.cs.cmu.edu/~rbhirang/). We would also like to cite the [reskin_sensor](https://github.com/raunaqbhirangi/reskin_sensor) library from which much of this library is derived.
