# rice-cooker-monitor
Monitor rice cooker with microcontroller

## English Instructions

1. Install [CircuitPython](https://circuitpython.org/) on your MCU of choice. The config in this repository uses ESP32
2. Modify the values in the top section of code.py for your settings.

| Name | Description |
| ---- | ----------- |
| SSID | Wifi Name |
| WEBHOOK_ENDPOINT | URL to send the message to, has to be discord webhook |
| CONNECTION_TEST_MSG | The message to send when the test button is pressed |
| COOKING_START_MSG | The message to send when cooking starts |
| COOKING_END_MSG | The message to send when cooking ends |
| TEST_BUTTON_PIN | Pin to attach a button to test connection |
| CT_PIN | Current transformer (CT) Pin |

```python
SSID = 'YOUR WIFI SSID HERE'
WEBHOOK_ENDPOINT = "DISCORD WEBHOOK URL HERE"

CONNECTION_TEST_MSG = '連線測試正常!'
COOKING_START_MSG = '已開始煮飯'
COOKING_END_MSG = '已完成煮飯'

TEST_BUTTON_PIN = board.D27
CT_PIN = board.D34
```
3. Upload the code to the MCU
4. Wire up the MCU to the current transformer and the test button. Default settings uses D27 for button and D34 for CT on ESP32
5. Wrap the current transformer around the neutral or hot wire of the rice cooker
6. Connect the MCU to a power source
