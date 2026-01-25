# L6470 MicroPython Driver (RP2040 / Raspberry Pi Pico)
日本語版はこちら → [README.ja.md](README.ja.md)

A simple **MicroPython driver** for the STMicroelectronics **L6470 stepper motor driver**,
designed for **Raspberry Pi Pico (RP2040)**.

This is a **pure MicroPython implementation** that directly controls the L6470 via SPI.

---

## Features

- SPI (Mode 3) communication with L6470
- Parameter configuration (ACC / DEC / MAX_SPEED / KVAL, etc.)
- Continuous rotation using RUN command
- BUSY pin synchronization
- Stable operation powered via USB
- Auto-generated `set_xxx()` / `get_xxx()` APIs


---

## Installation

### Installation

1. Clone the repository (Windows)
2. Copy the `l6470/ directory to /lib on your Pico.

/lib/l6470/

#Library Configuration
```
l6470/
├─ __init__.py
├─ l6470.py        # L6470 driver body
└─ registers.py   # Register and constant definitions
```


---

## How to install (using mpremote)

This library is **not yet compatible with MicroPython mip**.
Please install it manually using `mpremote`.


### 1. Get the repository (Windows)

```bat
git clone https://github.com/pukkunk/rp2040-l6470-micropython.git
cd rp2040-l6470-micropython
```

### 2. Connect to Pico (COM3 may change depending on your environment)
```bat
mpremote connect COM3 reset
```

### 3. Transfer the library to Pico
```bat
mpremote connect COM3 mkdir :/lib
mpremote connect COM3 cp -r l6470 :/lib
```

The internal configuration of Pico is as follows:
```
:/
  main.py
/lib
  l6470/
    __init__.py
    l6470.py
    registers.py
```

### 4. Transfer the sample program as main.py

```bat
mpremote connect COM3 cp example\pico_tracking.py :/main.py
```

### 5. Execution (Reset)
```bat
mpremote connect COM3 reset
```

##sample
example/minimal.py
```python
# example/minimal.py
from machine import SPI, Pin
from l6470 import L6470
import time

spi = SPI(0, baudrate=1_000_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT, value=1)
busy = Pin(0, Pin.IN)
motor = L6470(spi=spi, cs=cs, busy=busy)

motor.set_ACC(0x05)
motor.set_DEC(0x05)
motor.set_MAX_SPEED(0x200)
motor.run(L6470.FWD, 0x2000)

while True:
    time.sleep(1)
```

---

## Parts used

- **Raspberry Pi Pico**
- **Stepper Motor Drive Kit using L6470**
  - Purchased at Akizuki Electronics
- **Bipolar stepping motor SM-42BYG011**  
  - Purchased at Akizuki Electronics
- **Maximum 30V output boost switching power supply module (using NJW4131)**  
  - Purchased at Akizuki Electronics

## connection

### Raspberry Pi Pico ⇔ L6470 kit（CN10）

| Raspberry Pi Pico | function  | L6470 kit CN10 |
|------------------|---------|-------------------|
| GP00             | BUSY    | 1PIN : #BUSY/SYNC |
| （Not connected）| FLAG    | 2PIN : FLAG |
| GP02             | SCK     | 6PIN : CK |
| GP03             | MOSI    | 7PIN : SDI |
| GP04             | MISO    | 5PIN : SDO |
| GP05             | CS      | 8PIN : #CS |
| GND              | GND     | 3PIN : GND |
| GP06             | RESETN  | 10PIN : #STBY/RST |
| 3V3 (OUT)        | power supply    | 4PIN : EXT-VDD |
| （Not connected）| STCK    | 9PIN : STCK |

---

### Step-up switching power supply ⇔ L6470 kit (CN1)

| Step-up switching power supply | L6470 kit CN1 |
|-----------|------------------|
| out +    | VS+ |
| GND       | GND |


## Operating environment

- Raspberry Pi Pico / RP2040
- MicroPython
- L6470 Stepping Motor Driver

#license
MIT License
