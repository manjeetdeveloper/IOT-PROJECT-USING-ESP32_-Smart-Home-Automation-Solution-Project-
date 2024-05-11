import dht
from machine import Pin
import time
from BlynkLib import Blynk
import network

auth_token = 'ZJoZLGXXk2kO9bvRs0x-MU75kCBvVX7X'

# Function to connect to Wi-Fi network
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to WiFi:', ssid)

# Set up DHT11 sensor
dht_sensor = dht.DHT11(Pin(4))

# Set up gas sensor
gas_sensor_pin = Pin(15, Pin.IN)

# Set up IR sensor
ir_sensor_pin = Pin(19, Pin.IN)

# Set up buzzer
buzzer_pin = Pin(18, Pin.OUT)

# Set up relay module
relay_pin = Pin(5, Pin.OUT)
relay_pin.off()  # Initially turn off the relay

# Connect to Wi-Fi
wifi_ssid = '12 pro +'
wifi_password = '321321321'
connect_to_wifi(wifi_ssid, wifi_password)

# Set up Blynk
blynk = Blynk(auth_token)

# Function to read temperature and humidity from DHT11 sensor
def read_dht11():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

# Function to read gas sensor data
def read_gas_sensor():
    gas_level = gas_sensor_pin.value()
    return gas_level

# Function to read IR sensor data
def read_ir_sensor():
    obstacle_detected = ir_sensor_pin.value()
    return obstacle_detected

# Function to control buzzer based on gas detection
def control_buzzer(gas_level):
    if gas_level == 20:  # Gas detected
        buzzer_pin.on()  # Turn on the buzzer
    else:
        buzzer_pin.off()  # Turn off the buzzer

# Function to control buzzer based on obstacle detection
def control_buzzer_ir(obstacle_detected):
    if obstacle_detected:  # Obstacle detected
        buzzer_pin.on()  # Turn on the buzzer
    else:
        buzzer_pin.off()  # Turn off the buzzer

# Function to control relay based on temperature threshold
def control_relay(temperature):
    if temperature >= 25:
        relay_pin.on()  # Turn on the relay
    elif temperature <= 20:
        relay_pin.off()  # Turn off the relay

# Function to send temperature, humidity, gas, and IR sensor data to Blynk app
def update_blynk():
    temperature, humidity = read_dht11()
    gas_level = read_gas_sensor()
    obstacle_detected = read_ir_sensor()
    blynk.virtual_write(0, temperature)  # Virtual pin 0 for temperature
    blynk.virtual_write(1, humidity)     # Virtual pin 1 for humidity
    blynk.virtual_write(2, gas_level)     # Virtual pin 2 for gas level
    control_relay(temperature)            # Control relay based on temperature
    control_buzzer(gas_level)             # Control buzzer based on gas detection
    control_buzzer_ir(obstacle_detected)  # Control buzzer based on obstacle detection

# Callback function to handle data from Blynk app
def blynk_handle_data(pin, value):
    print('Received data from V{}: {}'.format(pin, value))
    if pin == 10:
        # Handle data received on virtual pin 10 (if necessary)
        pass
    elif pin == 11:
        # Handle data received on virtual pin 11 (if necessary)
        pass

# Register callback function to handle data from Blynk app
blynk.on('V10', blynk_handle_data)
blynk.on('V11', blynk_handle_data)

# Main loop
while True:
    update_blynk()
    blynk.run()
    time.sleep(1)  # Update readings every 1 second


