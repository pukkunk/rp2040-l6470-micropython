# example/minimal.py
from machine import SPI, Pin
from l6470 import registers as reg
from l6470 import L6470
import time

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
    reg.STEPMODE_SYNCEN_DISABLE |
    reg.STEPMODE_SYNCSEL0 |
    reg.STEPMODE_STEPSEL_DIV1_128_MICROSTEP
)
motor.set_param("STEP_MODE", step_mode)

# ------------------- モーター前進 -------------------
motor.run(L6470.FWD, 0x20)  # 安全低速で回転

# ------------------- 無限ループ -------------------
while True:
    time.sleep(1)

