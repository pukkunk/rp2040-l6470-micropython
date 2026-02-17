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
└─ l6470.py        # L6470 driver body
```


---

## How to install (using mpremote)

This library is **not compatible with MicroPython mip**.
Please install it manually using `mpremote`.


### 1. Transferred from github (Windows)

```
mpremote fs mkdir :/lib
mpremote mip install github:pukkunk/rp2040-l6470-micropython/l6470/__init__.py
mpremote mip install github:pukkunk/rp2040-l6470-micropython/l6470/l6470.py
```
### 2. Transfer the sample program as main.py
```
mpremote fs cp example\minimal.py :/main.py
```

### 3. Execution (Reset)
```
mpremote reset
```

The internal configuration of Pico is as follows:
```
:/
  main.py
/lib
  l6470/
    __init__.py
    l6470.py
```

##sample
```
# example/minimal.py
from machine import SPI, Pin
from l6470 import L6470
import time
from l6470 import (
    STEPMODE_SYNCEN_DISABLE,
    STEPMODE_SYNCSEL0,
    STEPMODE_STEPSEL_DIV1_128_MICROSTEP
)

spi = SPI(0, baudrate=1_000_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT, value=1)
busy = Pin(0, Pin.IN)
resetn = Pin(6, Pin.OUT, value=1)  # Pico GPIO6
motor = L6470(spi=spi, cs=cs, busy=busy, resetn=resetn)

# ------------------- パラメータ設定 -------------------
motor.set_ACC(0x05)        # ゆっくり立ち上げ
motor.set_DEC(0x05)        # ゆっくり停止
motor.set_MAX_SPEED(0x20)  # 上限を抑える（暴走防止）
motor.set_MIN_SPEED(0x00)  # 完全に停止可能
motor.set_FS_SPD(0x000)    # フルステップ遷移禁止

motor.set_KVAL_HOLD(0x50)
motor.set_KVAL_ACC(0x50)
motor.set_KVAL_RUN(0x40)
motor.set_KVAL_DEC(0x50)

# ------------------- ステップモード設定 -------------------
step_mode = (
    STEPMODE_SYNCEN_DISABLE |
    STEPMODE_SYNCSEL0 |
    STEPMODE_STEPSEL_DIV1_128_MICROSTEP
)
motor.set_param("STEP_MODE", step_mode)

# ------------------- モーター前進 -------------------
motor.run(L6470.FWD, 0x20)  # 安全低速で回転

# ------------------- 無限ループ -------------------
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

![](doc/img/Connection_Diagram.png)

## Operating environment

- Raspberry Pi Pico / RP2040
- MicroPython
- L6470 Stepping Motor Driver

#license
MIT License
