# main.py
from l6470 import L6470
import pico_define as pd

def main():

    motor = L6470()
    pd.led_on(pd.led, 0)

    print("L6470 instance created")

    # 1/128 microstep
    motor.set_param("STEP_MODE", 0b111)

    # 加速度・最大速度
    motor.set_param("ACC", 0x40)
    motor.set_param("DEC", 0x40)
    motor.set_param("MAX_SPEED", 0x100)

    # 現在座標取得
    pos = motor.get_param("ABS_POS")
    print("ABS_POS =", pos)
    motor.set_param("ALARM_EN", 0x00)
    status = motor.get_status()
    print("STATUS(after clear) = 0x%04X" % status)
    status = motor.get_status()
    print("STATUS = 0x%04X" % status)
    motor.run(1, 0x2000)  # 超低速

if __name__ == "__main__":
    main()

