import machine
import time

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

# L6470設定
L6470_STEPMODE_SYNCEN_ENABLE = (1 << 7)
L6470_STEPMODE_SYNCEN_DISABLE = (0 << 7)

L6470_STEPMODE_STEPSEL_FULL_STEP = 0x00
L6470_STEPMODE_STEPSEL_HALF_STEP = 0x01
L6470_STEPMODE_STEPSEL_DIV1_004_MICROSTEP = 0x02
L6470_STEPMODE_STEPSEL_DIV1_008_MICROSTEP = 0x03
L6470_STEPMODE_STEPSEL_DIV1_016_MICROSTEP = 0x04
L6470_STEPMODE_STEPSEL_DIV1_032_MICROSTEP = 0x05
L6470_STEPMODE_STEPSEL_DIV1_064_MICROSTEP = 0x06
L6470_STEPMODE_STEPSEL_DIV1_128_MICROSTEP = 0x07

L6470_STEPMODE_SYNCSEL0 = (0x00 << 4)
L6470_STEPMODE_SYNCSEL1 = (0x01 << 4)
L6470_STEPMODE_SYNCSEL2 = (0x02 << 4)
L6470_STEPMODE_SYNCSEL3 = (0x03 << 4)
L6470_STEPMODE_SYNCSEL4 = (0x04 << 4)
L6470_STEPMODE_SYNCSEL5 = (0x05 << 4)
L6470_STEPMODE_SYNCSEL6 = (0x06 << 4)
L6470_STEPMODE_SYNCSEL7 = (0x07 << 4)

# 定義
led = machine.Pin("LED", machine.Pin.OUT)  # LED端子を出力に設定

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



