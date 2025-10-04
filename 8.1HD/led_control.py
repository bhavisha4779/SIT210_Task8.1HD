import asyncio
from bleak import BleakClient, BleakScanner
import RPi.GPIO as GPIO
import time

# Use physical pin numbers
LED_PIN = 12   # Physical Pin 12 = GPIO18

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

# UUIDs must match Arduino sketch
SERVICE_UUID = "180C"
CHAR_UUID = "2A6E"

def handle_data(sender, data):
    lux = int.from_bytes(data, byteorder="little", signed=True)
    print(f"Lux: {lux}")

    # Thresholds:
    # Dark: LED OFF
    # Medium: Slow blink
    # Bright: Fast blink
    if lux < 50:
        # Dark → LED OFF
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

    elif lux < 200:
        # Medium light → Slow blink (1 second cycle)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

    else:
        # Bright light → Fast blink (0.2 second cycle)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.1)

async def run():
    print("Scanning for Arduino Nano 33 IoT...")
    devices = await BleakScanner.discover()

    arduino = None
    for d in devices:
        if "Nano33_BH1750" in d.name:  
            arduino = d
            break

    if not arduino:
        print("Arduino not found. Make sure it's powered and advertising.")
        return

    print(f"Connecting to {arduino.name} ({arduino.address})")

    async with BleakClient(arduino.address) as client:
        print("Connected!")

        await client.start_notify(CHAR_UUID, handle_data)

        print("Receiving data... Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(1)

try:
    asyncio.run(run())
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
