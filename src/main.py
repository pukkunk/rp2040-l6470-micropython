from l6470 import L6470
import pico_define as pd
import time
import machine

# ピン定義
PIN_SCK = 2     # → GPIO2 (GP2)    # pin No #04
PIN_MOSI = 3    # → GPIO3 (GP3)    # pin No #05
PIN_MISO = 4    # → GPIO4 (GP4)    # pin No #06
PIN_CS = 5      # → GPIO5 (GP5)    # pin No #07

GP00 = 0  # pin No #01
GP06 = 6  # pin No #0957

PIN_BUSY = GP00
PIN_RESETN = GP06

# SPI設定
SPI_PORT0 = 0  # SPIポート名を文字列で定義
READ_BIT = 0x80

# SPI Max freq = 5MHz
SPI_CLK_10MHZ = 10000000
SPI_CLK_06MHZ = 6000000
SPI_CLK_04MHZ = 4000000
SPI_CLK_01MHZ = 1000000

def main():
    motor = L6470(
        spi_port = 0,
        sck      = PIN_SCK,
        mosi     = PIN_MOSI,
        miso     = PIN_MISO,
        cs       = PIN_CS,
        busy     = PIN_BUSY,
        resetn  = PIN_RESETN,
        baudrate= SPI_CLK_01MHZ
    )
    led = machine.Pin("LED", machine.Pin.OUT)  # LED端子を出力に設定
    led_on(led, 0)

    print("L6470 instance created")
    led_toggle(led, 5, 1)

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

    motor.set_ACC(0x05)   # ゆっくり立ち上げ
    motor.set_DEC(0x05)   # ゆっくり止める
    motor.set_MAX_SPEED(0x20)  # 上限を抑える（暴走防止）
    motor.set_MIN_SPEED(0x00)  # 完全に0
    motor.set_FS_SPD(0x000)  # フルステップ遷移禁止

    motor.set_KVAL_HOLD(0x50)
    motor.set_KVAL_ACC(0x50)
    motor.set_KVAL_RUN(0x40)

    step_mode = (
        pd.L6470_STEPMODE_SYNCEN_DISABLE |
        pd.L6470_STEPMODE_SYNCSEL0 |
        pd.L6470_STEPMODE_STEPSEL_DIV1_128_MICROSTEP
    )
    motor.set_param("STEP_MODE", step_mode)

    speed = 0x2000  # 超低速
    motor.run(L6470.FWD, speed)

    time.sleep(2)  # 回り始めるまで待つ

    # 追尾用（低振動）
    motor.set_KVAL_HOLD(0x30)
    motor.set_KVAL_ACC(0x30)
    motor.set_KVAL_RUN(0x28)

    print("END")

# ------- for pico onboard LED
def led_toggle(led, count: int, cycle_sec: float, duty_high_per: int = 50, duty_low_per: int = 50):
    """LEDを指定回数点滅させる"""
    for i in range(count):  # 修正 #修正
        led_value = led.value()  # LEDの現在の状態を取得
        led_value = 1 - led_value  # 状態を反転
        led.value(led_value)
        time.sleep(cycle_sec * duty_high_per / (duty_high_per + duty_low_per))
        led_value = 1 - led_value  # 状態を再度反転
        led.value(led_value)
        time.sleep(cycle_sec * duty_low_per / (duty_high_per + duty_low_per))

def led_on(led, wait_time_sec: float):
    """LEDを指定時間点灯させる"""
    led.value(1)  # LEDを点灯
    time.sleep(wait_time_sec)

def led_off(led, wait_time_sec: float):
    """LEDを指定時間消灯させる"""
    led.value(0)  # LEDを消灯
    time.sleep(wait_time_sec)
# ------- for pico onboard LED end

if __name__ == "__main__":
    main()

