# example/minimal.py
from machine import SPI, Pin
from l6470 import registers as reg
from l6470 import L6470
import time

def main():
    spi = SPI(0, baudrate=1_000_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs = Pin(5, Pin.OUT, value=1)
    busy = Pin(0, Pin.IN)
    resetn = Pin(6, Pin.OUT, value=1)  # Pico GPIO6
    motor = L6470(spi=spi, cs=cs, busy=busy, resetn=resetn)

    # ------------------- パラメータ設定 -------------------
    print("aftere reset reg value")
    dump_all_params(motor)
    # set Reset value
    print("set reg value:init val")
    motor.set_ABS_POS   (0x00)
    motor.set_EL_POS    (0x00)
    motor.set_MARK      (0x00)
    motor.set_ACC       (0x08A)
    motor.set_DEC       (0x08A)
    motor.set_MAX_SPEED (0x041)
    motor.set_MIN_SPEED (0x000)
    motor.set_FS_SPD    (0x027)
    motor.set_KVAL_HOLD (0x29)
    motor.set_KVAL_RUN  (0x29)
    motor.set_KVAL_ACC  (0x29)
    motor.set_KVAL_DEC  (0x29)
    motor.set_INT_SPEED (0x0408)
    motor.set_ST_SLP    (0x19)
    motor.set_FN_SLP_ACC(0x29)
    motor.set_FN_SLP_DEC(0x29)
    motor.set_K_THERM   (0x0)
    motor.set_OCD_TH    (0x8)
    motor.set_STALL_TH  (0x40)
    motor.set_STEP_MODE (0x7)
    motor.set_ALARM_EN  (0xFF)
    motor.set_CONFIG    (0x2E88)
    # get Reset value
    #reg_val = motor.get_ABS_POS()
    #reg_val = motor.get_EL_POS()
    #reg_val = motor.get_MARK()
    #reg_val = motor.get_SPEED()
    #reg_val = motor.get_ACC()
    #reg_val = motor.get_DEC()
    #reg_val = motor.get_MAX_SPEED()
    #reg_val = motor.get_MIN_SPEED()
    #reg_val = motor.get_FS_SPD()
    #reg_val = motor.get_KVAL_HOLD()
    #reg_val = motor.get_KVAL_RUN()
    #reg_val = motor.get_KVAL_ACC()
    #reg_val = motor.get_KVAL_DEC()
    #reg_val = motor.get_INT_SPEED()
    #reg_val = motor.get_ST_SLP()
    #reg_val = motor.get_FN_SLP_ACC()
    #reg_val = motor.get_FN_SLP_DEC()
    #reg_val = motor.get_K_THERM()
    #reg_val = motor.get_ADC_OUT()
    #reg_val = motor.get_OCD_TH()
    #reg_val = motor.get_STALL_TH()
    #reg_val = motor.get_STEP_MODE()
    #reg_val = motor.get_ALARM_EN()
    #reg_val = motor.get_CONFIG()
    #reg_val = motor.get_STATUS()
    print("get reg value:init val")
    dump_all_params(motor)

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

def dump_all_params(motor):
    for name, (_, _, access) in motor._L6470_RAW.items():
        if "R" not in access:
            continue

        # get_XXX メソッド名を作る
        getter_name = f"get_{name}"

        # メソッド取得
        getter = getattr(motor, getter_name)

        # 読み出し
        val = getter()
        print(f"{name:12s} = 0x{val:X} ({val})")

if __name__ == "__main__":
    main()

