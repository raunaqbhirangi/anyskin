/*
  AnySkin Board Example Code
  By: Raunaq Bhirangi
  Date: October 1, 2024
  License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

  Library: Heavily based on original MLX90393 library from Theodore Yapo (https://github.com/tedyapo/arduino-MLX90393)
  Use this fork (https://github.com/tesshellebrekers/arduino-MLX90393) to access additional burst mode commands

  Read the XYZ magnetic flux fields and temperature across all five chips on the 5X AnySkin board
  Print binary data over serial port
*/

#include <Wire.h>
#include <MLX90393.h>

#define Serial SERIAL_PORT_USBVIRTUAL

const int numChips = 5; //Number of MLX90393 chips on the 5X AnySkin board

MLX90393 mlx[numChips]; //Create an array of five MLX90393 objects
MLX90393::txyz data[numChips] = {0,0,0,0}; //Create an array of five structures, called data, of four floats (t, x, y, and z)

uint8_t mlx_i2c[5] = {0x0C, 0x0D, 0x0E, 0x0F, 0x10}; // these are the I2C addresses of the five chips that share one I2C bus

void setup()
{
  //Start serial port and wait until user opens it
  Serial.begin(115200);
  while (!Serial) {
    delay(5);
  }

  //Start default I2C bus for your board, set to fast mode (400kHz)
  Wire.begin();
  Wire.setClock(400000);
  delay(10);

  //start chips given address, -1 for no DRDY pin, and I2C bus object to use
  byte status;
  for(int i = 0; i < numChips; i++)
  {
    status = mlx[i].begin(mlx_i2c[i], -1, Wire);
    mlx[i].startBurst(0xF);
    //default gain and digital filtering set up in the begin() function of library. Adjust here is you want to change them
    // mlx[i].setGain(5); //accepts [0,7]
    // mlx[i].setDigitalFiltering(5); // accepts [2,7]. refer to datasheet for hall configurations
  }
}

void loop()
{
  //continuously read the most recent data from the data registers and save to data
  for(int i = 0; i < numChips; i++)
  {
    mlx[i].readBurstData(data[i]);
    Serial.write((byte*)&data[i], sizeof(data[i]));
  }
  Serial.println();
}
