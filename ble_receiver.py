import asyncio
from bleak import BleakClient, BleakScanner

# Define the UUIDs & device name
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID_TX = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
DEVICE_NAME = "XIAO_ESP32S3"


# Callback function to handle received data
def handle_rx(_, data):
    print("Received data:", data)
    with open("received_image.jpg", "wb") as f:
        f.write(data)


async def scan_for_device(timeout=30):
    print(f"Scanning for {DEVICE_NAME}...")
    devices = await BleakScanner.discover(timeout)
    for device in devices:
        print(f"Found device: {device.address} - {device.name}")
        if device.name and DEVICE_NAME in device.name:
            return device
    return None


async def main():
    device = await scan_for_device(timeout=30)

    if device is None:
        print(f"Device '{DEVICE_NAME}' not found")
        return

    esp32_address = device.address

    async with BleakClient(esp32_address) as client:
        print(f"Connected to {esp32_address}")

        # Subscribe to notifications
        await client.start_notify(CHARACTERISTIC_UUID_TX, handle_rx)

        # Keep the connection open for some time
        await asyncio.sleep(60)

        # Stop notifications
        await client.stop_notify(CHARACTERISTIC_UUID_TX)


asyncio.run(main())
