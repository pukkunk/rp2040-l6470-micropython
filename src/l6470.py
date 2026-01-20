# l6470.py
# L6470 Stepper Motor Driver (MicroPython)
# Datasheet based, clean-room implementation

from machine import SPI, Pin
import pico_define as pd
import time

class L6470:
    REV = 0  # 逆回転
    FWD = 1  # 正転

    CMD_NOP          = 0x00
    CMD_HARD_HIZ     = 0xA8
    CMD_SOFT_HIZ     = 0xA0
    CMD_SET_PARAM    = 0x00
    CMD_GET_PARAM    = 0x20
    CMD_RESET_DEVICE = 0xC0
    CMD_GET_STATUS   = 0xD0
    CMD_RUN          = 0x50  # RUN + direction

    # 内部パラメータマップ (address, bit_length, access)
    _L6470_RAW = {
        "ABS_POS"   :(0x01, 22, "R, WS"),
        "EL_POS"    :(0x02, 9,  "R, WS"),
        "MARK"      :(0x03, 22, "R, WR"),
        "SPEED"     :(0x04, 20, "R"),
        "ACC"       :(0x05, 12, "R, WS"),
        "DEC"       :(0x06, 12, "R, WS"),
        "MAX_SPEED" :(0x07, 10, "R, WR"),
        "MIN_SPEED" :(0x08, 13, "R, WS"),
        "FS_SPD"    :(0x15, 10, "R, WR"),
        "KVAL_HOLD" :(0x09, 8,  "R, WR"),
        "KVAL_RUN"  :(0x0A, 8,  "R, WR"),
        "KVAL_ACC"  :(0x0B, 8,  "R, WR"),
        "KVAL_DEC"  :(0x0C, 8,  "R, WR"),
        "INT_SPEED" :(0x0D, 14, "R, WH"),
        "ST_SLP"    :(0x0E, 8,  "R, WH"),
        "FN_SLP_ACC":(0x0F, 8,  "R, WH"),
        "FN_SLP_DEC":(0x10, 8,  "R, WH"),
        "K_THERM"   :(0x11, 4,  "R, WR"),
        "ADC_OUT"   :(0x12, 5,  "R"),
        "OCD_TH"    :(0x13, 4,  "R, WR"),
        "STALL_TH"  :(0x14, 7,  "R, WR"),
        "STEP_MODE" :(0x16, 8,  "R, WH"),
        "ALARM_EN"  :(0x17, 8,  "R, WS"),
        "CONFIG"    :(0x18,16,  "R, WH"),
        "STATUS"    :(0x19,16,  "R"),
    }

    def __init__(
        self,
        spi_port,
        sck,
        mosi,
        miso,
        cs,
        busy,
        resetn,
        baudrate=1_000_000,
    ):

        print("L6470 init")

        # --- GPIO ---
        self.cs     = Pin(cs, Pin.OUT, value=1)
        self.busy   = Pin(busy, Pin.IN)
        self.resetn = Pin(resetn, Pin.OUT, value=1)

        # --- SPI (Mode 3) ---
        self.spi = SPI(
            spi_port,
            baudrate=baudrate,
            polarity=1,   # CPOL=1
            phase=1,      # CPHA=1
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(sck),
            mosi=Pin(mosi),
            miso=Pin(miso),
        )

        # --- Hardware reset ---
        self._hardware_reset()
        self.reset_device()

    # -------------------------------------------------
    # Internal utilities
    # -------------------------------------------------
    def _select(self):
        self.cs.value(0)

    def _deselect(self):
        self.cs.value(1)

    def _hardware_reset(self):
        self.resetn.value(0)
        time.sleep_ms(100)
        self.resetn.value(1)
        time.sleep_ms(10)

    def _wait_busy_release(self, sleep_us=50):
        while self.busy.value() == 0:
            time.sleep_us(sleep_us)

    # -------------------------------------------------
    # Parameter access
    # -------------------------------------------------
    def set_param(self, name: str, value: int):
        """
        Set L6470 parameter by name
        """
        if name not in self._L6470_RAW:
            raise ValueError("Unknown parameter: " + name)
        addr, bit_len, _ = self._L6470_RAW[name]
        byte_len = (bit_len + 7) // 8
        max_val = (1 << bit_len) - 1
        if value < 0 or value > max_val:
            raise ValueError(f"{name} out of range (0..{max_val})")

        # データをまとめて送信
        data = [self.CMD_SET_PARAM | addr] + [(value >> (8*(byte_len-i-1))) & 0xFF for i in range(byte_len)]
        self._select()
        try:
            self.spi.write(bytes(data))
        finally:
            self._deselect()

    def get_param(self, name: str) -> int:
        """
        Read L6470 parameter by name
        """
        if name not in self._L6470_RAW:
            raise ValueError("Unknown parameter: " + name)
        addr, bit_len, _ = self._L6470_RAW[name]
        byte_len = (bit_len + 7) // 8
        value = 0

        self._select()
        try:
            self.spi.write(bytes([self.CMD_GET_PARAM | addr]))
            for _ in range(byte_len):
                b = self.spi.read(1)[0]
                value = (value << 8) | b
        finally:
            self._deselect()
        return value

    def get_status(self) -> int:
        self._wait_busy_release()
        self._select()
        try:
            self.spi.write(bytes([self.CMD_GET_STATUS]))
            data = self.spi.read(2)
        finally:
            self._deselect()
        return (data[0] << 8) | data[1]

    # -------------------------------------------------
    # Motion
    # -------------------------------------------------
    def exit_hiz(self):
        # ダミーRUNでHi-Z解除
        data = [self.CMD_RUN | self.FWD, 0x00, 0x00, 0x01]
        self._select()
        try:
            self.spi.write(bytes(data))
        finally:
            self._deselect()
        time.sleep_ms(1)

    def run(self, direction: int, speed: int):
        self._check_direction(direction)
        self._run_internal(direction, speed)
        self._wait_busy_release()

    def run_no_wait(self, direction: int, speed: int):
        self._check_direction(direction)
        self._run_internal(direction, speed)

    def _run_internal(self, direction: int, speed: int):
        if speed > 0xFFFFF:
            speed = 0xFFFFF
        data = [self.CMD_RUN | (direction & 0x01),
                (speed >> 16) & 0xFF,
                (speed >> 8) & 0xFF,
                speed & 0xFF]
        self._select()
        try:
            self.spi.write(bytes(data))
        finally:
            self._deselect()

    def _check_direction(self, direction: int):
        if direction not in (self.REV, self.FWD):
            raise ValueError(f"Invalid direction: {direction}")

    def reset_device(self):
        data = [self.CMD_NOP]*4 + [self.CMD_RESET_DEVICE]
        self._select()
        try:
            self.spi.write(bytes(data))
        finally:
            self._deselect()
        self._wait_busy_release()

    def wait_motion_end(self):
        while self.busy.value() == 0:
            time.sleep_ms(1)

# ------------------------------
# Auto-generate set/get functions
# ------------------------------
def _make_setter(name):
    def setter(self, val):
        return self.set_param(name, val)
    return setter

def _make_getter(name):
    def getter(self):
        return self.get_param(name)
    return getter

for pname, (addr, bits, access) in L6470._L6470_RAW.items():
    if "W" in access:
        setattr(L6470, f"set_{pname}", _make_setter(pname))
    if "R" in access:
        setattr(L6470, f"get_{pname}", _make_getter(pname))
