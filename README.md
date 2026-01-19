# L6470 MicroPython Driver (RP2040 / Raspberry Pi Pico)

STMicroelectronics **L6470 ステッピングモータドライバ** を  
**Raspberry Pi Pico (RP2040) + MicroPython** から制御するための  
シンプルなドライバ実装です。

---

## 現在できること

- SPI（Mode3）による L6470 制御
- パラメータ設定（ACC / DEC / MAX_SPEED / KVAL など）
- RUN コマンドによる連続回転
- BUSY ピンによる動作同期
- USB 給電環境でも安定して回転
- 自動生成された `set_xxx()` / `get_xxx()` API が利用可能

---

## 動作環境

- Raspberry Pi Pico / RP2040
- MicroPython
- L6470 ステッピングモータドライバ

---

ピン番号は `pico_define.py` に定義

