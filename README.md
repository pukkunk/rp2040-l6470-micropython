# L6470 MicroPython Driver (RP2040 / Raspberry Pi Pico)

STMicroelectronics **L6470 ステッピングモータドライバ** を  
**Raspberry Pi Pico (RP2040) + MicroPython** から制御するための  
シンプルなドライバ実装です。

Pure MicroPython 実装で、SPI 経由で L6470 を直接制御します。

---

## 現在できること

- SPI（Mode3）による L6470 制御
- パラメータ設定（ACC / DEC / MAX_SPEED / KVAL など）
- RUN コマンドによる連続回転
- BUSY ピンによる動作同期
- USB 給電環境でも安定して回転
- 自動生成された `set_xxx()` / `get_xxx()` API が利用可能


---

## インストール方法

### 方法1：mip（推奨）

```
python
import mip
mip.install("github:pukkunk/rp2040-l6470-micropython")
```

### 方法2：手動コピー

l6470/ ディレクトリを Pico の /lib にコピーしてください。

/lib/l6470/

#ライブラリ構成
```
l6470/
├─ __init__.py
├─ l6470.py        # L6470 ドライバ本体
└─ registers.py   # レジスタ・定数定義
```

---

## 使用部品

- **Raspberry Pi Pico**
- **L6470 使用 ステッピングモータードライブキット**  
  - 秋月電子で購入
- **バイポーラー ステッピングモーター SM-42BYG011**  
  - 秋月電子で購入
- **最大 30V 出力 昇圧型スイッチング電源モジュール（NJW4131 使用）**  
  - 秋月電子で購入

## 接続

### Raspberry Pi Pico ⇔ L6470 キット（CN10）

| Raspberry Pi Pico | 機能    | L6470 キット CN10 |
|------------------|---------|-------------------|
| GP00             | BUSY    | 1PIN : #BUSY/SYNC |
| （未接続）       | FLAG    | 2PIN : FLAG |
| GP02             | SCK     | 6PIN : CK |
| GP03             | MOSI    | 7PIN : SDI |
| GP04             | MISO    | 5PIN : SDO |
| GP05             | CS      | 8PIN : #CS |
| GND              | GND     | 3PIN : GND |
| GP06             | RESETN  | 10PIN : #STBY/RST |
| 3V3 (OUT)        | 電源    | 4PIN : EXT-VDD |
| （未接続）       | STCK    | 9PIN : STCK |

---

### 昇圧型スイッチング電源 ⇔ L6470 キット（CN1）

| 昇圧型電源 | L6470 キット CN1 |
|-----------|------------------|
| 出力 +    | VS+ |
| GND       | GND |


## 動作環境

- Raspberry Pi Pico / RP2040
- MicroPython
- L6470 ステッピングモータドライバ

#ライセンス
MIT License
