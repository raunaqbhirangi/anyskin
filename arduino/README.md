# Getting Started with Arduino for AnySkin

First, install Arduino IDE and the relevant board packages in order to upload code to your microcontroller.

We tested the following on [Trinket M0](https://www.adafruit.com/product/3500) and [QT Py](https://www.adafruit.com/product/4600) from Adafruit.
  They have excellent tutorials for setting up these boards with your Arduino IDE. Follow [this one for the Trinket M0](https://learn.adafruit.com/adafruit-trinket-m0-circuitpython-arduino/arduino-ide-setup) and [this one for the QT Py](https://learn.adafruit.com/adafruit-qt-py/arduino-ide-setup).

## Parts

We generally recommend the QT Py as it has an on-board Qwiic/STEMMA connector and USB-C connector, and does not require any soldering. Parts list for these two boards is as follows:

### Trinket M0
 - [Qwiic/STEMMA to breadboard cable](https://www.adafruit.com/product/4209)
 - micro-USB to USB-A cable
 - AnySkin circuit board

### Qt Py
 - [Qwiic/STEMMA cable](https://www.adafruit.com/product/4401)
 - USB-C to USB-A cable
 - AnySkin circuit board

## Installing Arduino Library (submodule)

The library for the magnetometers is included as a submodule of this repo. Install the submodule
```
git submodule update --init
```
Move this library into your local libraries folder for your Arduino installation.

## Finding your port

<b>Linux:</b> `ls /dev/ | grep -e ACM -e USB`. This is generally `/dev/ttyACM0` or `/dev/ttyUSB0`. <br>If you get a `can't open device "<port>": Permission denied` error, modify permissions to allow read and write on that port: `sudo chmod a+rw <port>`
<br><br> <b>MacOS:</b> `ls /dev/ | grep cu.usb`. This is generally `cu.usbmodem*`.
<br><br> <b>Windows:</b> Open Device Manager. Click `View` and select `Show Hidden Devices`. Locate `Ports (COM & LPT)`. Note the `COM` port corresponding to the QT Py.

If you have no other devices connected, this should give you a single path. If you see multiple, disconnect the microcontroller and run the command again. Reconnect the microcontroller and re-run the command. The new device between the two lists is your port.
