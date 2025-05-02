import wifi
import adafruit_requests
import ssl
import socketpool
import json
import digitalio
import board
import time
import analogio

SSID = 'YOUR WIFI SSID HERE'
WEBHOOK_ENDPOINT = "DISCORD WEBHOOK URL HERE"

CONNECTION_TEST_MSG = '連線測試正常!'
COOKING_START_MSG = '已開始煮飯'
COOKING_END_MSG = '已完成煮飯'

TEST_BUTTON_PIN = board.D27
CT_PIN = board.D34

requests = None

def wifi_connect(ssid):
    mac_str = ''.join([hex(i)[2:] for i in wifi.radio.mac_address])
    print(f'Wifi MAC Address: {mac_str}')
    print(f'Connecting to {ssid}...')
    wifi.radio.connect(ssid=ssid)
    print(f'Connected with IP: {wifi.radio.ipv4_address}')

    global requests

    pool = socketpool.SocketPool(wifi.radio)
    context = ssl.create_default_context()
    requests = adafruit_requests.Session(pool, context)

def send_webhook(message):
    headers = {"Content-Type": "application/json"}
    body = {"content": message}
    
    global requests
    
    body_json = json.dumps(body)
    requests.post(WEBHOOK_ENDPOINT, headers=headers, data=body_json)

button = digitalio.DigitalInOut(TEST_BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

button_last = False


adc = analogio.AnalogIn(CT_PIN)
adc_last = False
adc_now = False
ADC_THR_HI = 12000
ADC_THR_LO = 8000

wifi_connect(SSID)

while True:
    
    if not wifi.radio.connected:
        print(f'Wifi disconnected, reconnecting...')
        wifi_connect(SSID)
    
    if button_last and not button.value:
        send_webhook(CONNECTION_TEST_MSG)
    
    button_last = button.value
    
    if adc.value > ADC_THR_HI:
        adc_now = True
    elif adc.value < ADC_THR_LO:
        adc_now = False
    
    if adc_now and not adc_last:
        send_webhook(COOKING_START_MSG)
    
    elif adc_last and not adc_now:
        send_webhook(COOKING_END_MSG)
        
    adc_last = adc_now

    time.sleep(0.1)
    
