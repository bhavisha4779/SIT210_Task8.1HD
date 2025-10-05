import asyncio, time
from bleak import BleakClient, BleakScanner
import RPi.GPIO as GPIO

LED = 12  # physical pin 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

SERVICE = "180C"
CHAR = "2A6E"

def on_data(sender, data):
    lux = int.from_bytes(data, "little", signed=True)
    print(f"Lux: {lux}")

    if lux < 50:           # dark
        GPIO.output(LED, 0)
        time.sleep(0.5)
    elif lux < 200:        # medium
        GPIO.output(LED, 1)
        time.sleep(0.5)
        GPIO.output(LED, 0)
        time.sleep(0.5)
    else:                  # bright
        GPIO.output(LED, 1)
        time.sleep(0.1)
        GPIO.output(LED, 0)
        time.sleep(0.1)

async def main():
    print("Scanning for Arduino...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if "Nano33_BH1750" in d.name), None)
    if not target:
        print("Arduino not found")
        return
    print(f"Connecting to {target.name}")
    async with BleakClient(target.address) as client:
        print("Connected!")
        await client.start_notify(CHAR, on_data)
        while True:
            await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopped")
finally:
    GPIO.cleanup()



