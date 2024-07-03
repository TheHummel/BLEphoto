import asyncio
from bleak import BleakClient, BleakScanner

# Define the UUIDs & device name
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID_TX = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
DEVICE_NAME = "XIAO_ESP32S3"

# buffer to store received image data
image_data = bytearray()


# Callback function to handle received data
def handle_rx(_, data):
    global image_data
    image_data.extend(data)
    print("Received data chunk:", len(data))


async def scan_for_device(timeout=30):
    print(f"Scanning for {DEVICE_NAME}...")
    devices = await BleakScanner.discover(timeout)
    for device in devices:
        print(f"Found device: {device.address} - {device.name}")
        if device.name and DEVICE_NAME in device.name:
            return device
    return None


async def main():
    global image_data
    device = await scan_for_device(timeout=60)

    if device is None:
        print(f"Device '{DEVICE_NAME}' not found")
        return

    esp32_address = device.address

    async with BleakClient(esp32_address) as client:
        print(f"Connected to {esp32_address}")

        # subscribe to notifications
        await client.start_notify(CHARACTERISTIC_UUID_TX, handle_rx)

        # keep the connection open for some time
        await asyncio.sleep(60)

        # stop notifications
        await client.stop_notify(CHARACTERISTIC_UUID_TX)

    # save received image data to file
    with open("received_image.jpg", "wb") as f:
        f.write(image_data)
    print("Image saved as received_image.jpg")


asyncio.run(main())
