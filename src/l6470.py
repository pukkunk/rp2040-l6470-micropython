# l6470.py
# L6470 Stepper Motor Driver (MicroPython)
# Datasheet based, clean-room implementation

from machine import SPI, Pin
import time
import pico_define as pd   # ← 既存定義を使う前提

class L6470:
    def __init__(self, spi_port=0,
                 sck=pd.PIN_SCK,
                 mosi=pd.PIN_MOSI,
                 miso=pd.PIN_MISO,
                 cs=pd.PIN_CS,
                 busy=pd.PIN_BUSY,
                 resetn=pd.PIN_RESETN,
                 baudrate=1_000_000):

        print("L6470 init")

        # --- GPIO ---
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.resetn = Pin(resetn, Pin.OUT, value=1)
        self.busy = Pin(busy, Pin.IN)

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
        pd.led_toggle(pd.led, 5, 1)  # LEDを3回点滅 #修正
        self._hardware_reset()
        self.reset_device()

    # -------------------------------------------------
    # Internal utilities
    # -------------------------------------------------
    _L6470_RAW = {
        # NAME        :(address, bit_length)
        "ABS_POS"   :(0x01, 22),
        "EL_POS"    :(0x02, 9),
        "MARK"      :(0x03, 22),
        "SPEED"     :(0x04, 20),
        "ACC"       :(0x05, 12),
        "DEC"       :(0x06, 12),
        "MAX_SPEED" :(0x07, 10),
        "MIN_SPEED" :(0x08, 13),
        "FS_SPD"    :(0x15, 10),
        "KVAL_HOLD" :(0x09, 8),
        "KVAL_RUN"  :(0x0A, 8),
        "KVAL_ACC"  :(0x0B, 8),
        "KVAL_DEC"  :(0x0C, 8),
        "INT_SPEED" :(0x0D, 14),
        "ST_SLP"    :(0x0E, 8),
        "FN_SLP_ACC":(0x0F, 8),
        "FN_SLP_DEC":(0x10, 8),
        "K_THERM"   :(0x11, 4),
        "ADC_OUT"   :(0x12, 5),
        "OCD_TH"    :(0x13, 4),
        "STALL_TH"  :(0x14, 7),
        "STEP_MODE" :(0x16, 8),
        "ALARM_EN"  :(0x17, 8),
        "CONFIG"    :(0x18, 16),
        "STATUS"    :(0x19, 16),
    }

    CMD_NOP          = 0x00
    CMD_SET_PARAM    = 0x00
    CMD_GET_PARAM    = 0x20
    CMD_RESET_DEVICE = 0xC0
    CMD_GET_STATUS   = 0xD0

    def _select(self):
        self.cs.value(0)

    def _deselect(self):
        self.cs.value(1)

    def _hardware_reset(self):
        self.resetn.value(0)
        time.sleep_ms(10)
        time.sleep_ms(10000)
        self.resetn.value(1)
        time.sleep_ms(10)
      
    def _spi_write(self, data: int):
        self.spi.write(bytearray([data]))

    def _send_u(self, value: int):
        """BUSY無視で1バイト送信"""
        self.cs.value(0)
        self.spi.write(bytes([value & 0xFF]))
        self.cs.value(1)
        time.sleep_us(2)

    def reset_device(self):
        """SOFT_RESET (ResetDevice command)"""
        self._send_u(self.CMD_NOP)          #修正
        self._send_u(self.CMD_NOP)          #修正
        self._send_u(self.CMD_NOP)          #修正
        self._send_u(self.CMD_NOP)          #修正
        self._send_u(self.CMD_RESET_DEVICE) #修正

    def set_param(self, name: str, value: int):
        """
        Set L6470 parameter by name
        """
        if name not in self._L6470_RAW:
            raise ValueError("Unknown parameter: " + name)

        addr, bit_len = self._L6470_RAW[name]
        byte_len = (bit_len + 7) // 8
        max_val = (1 << bit_len) - 1

        if value < 0 or value > max_val:
            raise ValueError(f"{name} out of range (0..{max_val})")

        # send command
        self._send_u(self.CMD_SET_PARAM | addr)

        # send MSB first
        for shift in range((byte_len - 1) * 8, -1, -8):
            self._send_u((value >> shift) & 0xFF)

    def get_param(self, name: str) -> int:
        """
        Read L6470 parameter by name
        """
        if name not in self._L6470_RAW:
            raise ValueError("Unknown parameter: " + name)

        addr, bit_len = self._L6470_RAW[name]
        byte_len = (bit_len + 7) // 8

        value = 0
        self._send_u(self.CMD_GET_PARAM | addr)

        for _ in range(byte_len):
            self.cs.value(0)
            b = self.spi.read(1)[0]
            self.cs.value(1)
            value = (value << 8) | b

        return value

    def get_status(self) -> int:
        """
        Read STATUS register (and clear FLAG)
        """
        self.cs.value(0)
        self.spi.write(bytes([self.CMD_GET_STATUS]))
        data = self.spi.read(2)
        self.cs.value(1)
        return (data[0] << 8) | data[1]

    def _wait_busy_release(self):
        while self.busy.value() == 0:
            pass

