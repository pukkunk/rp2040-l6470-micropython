from l6470 import L6470
import pico_define as pd
import time

def main():
    motor = L6470()
    pd.led_on(pd.led, 0)

    print("L6470 instance created")
    motor.set_STEP_MODE(0b111)


#   motor.set_param("ACC", 0x40)
#   motor.set_param("DEC", 0x40)
#   motor.set_param("MAX_SPEED", 0x40)
#   motor.set_param("MIN_SPEED", 0x01)
#   motor.set_param("FS_SPD", 0x3FF)
#
#   motor.set_param("KVAL_HOLD", 0x50)
#   motor.set_param("KVAL_RUN", 0x50)
#   motor.set_param("KVAL_ACC", 0x50)
#   motor.set_param("KVAL_DEC", 0x50)
#
#   motor.set_param("STEP_MODE", 0x03)  # 1/16

    motor.set_ACC(0x40)
    motor.set_DEC(0x40)
    motor.set_MAX_SPEED(0x40)
    motor.set_MIN_SPEED(0x01)
    motor.set_FS_SPD(0x3FF)

    motor.set_KVAL_HOLD(0x50)
    motor.set_KVAL_RUN(0x50)
    motor.set_KVAL_ACC(0x50)
    motor.set_KVAL_DEC(0x50)

    motor.set_STEP_MODE(0x03)   # 1/16

    speed = 0x2000  # 超低速
    motor.run(L6470.FWD, speed)

    print("END")

if __name__ == "__main__":
    main()

