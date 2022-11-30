# Simple program written in MicroPython for LED RGB color change

## Tools

1. MicroPython
2. Microcontroller: raspberry pi pico (RP2040)

## Video with an example of operating the device

https://user-images.githubusercontent.com/71873238/204652224-ee3208d4-c521-40b6-9d87-61d3b26293b4.mp4

## Circuit diagram

![diagram](diagram.png "diagram")

You can change resistors to fit your diode.

## Operation of buttons and potentiometer

1. **Button ON/OFF** - Turn on the LED/ Turn down.
2. **Button change color/Save**:
    - **Press and release** - change color component: red, green and blue
    - **Press and hold 3 seconds** - save color
3. **Potentiometer** - fit intensity of color component

The device remembers the saved color after turning off the power.

## Scripts

1. **main.py** - file with program
2. **delete_all_files_from_pico.py** - script removing all files from raspberry pi pico

