# Author: Sameer Khandekar
# MIT License

# import for async
import asyncio

# import library for GPIO
import RPi.GPIO as GPIO

# time library
import time

# Port of PIR i.e. GPIO14
pir_port = 14

# import for environment variable
import os

#import IoTHub client
from azure.iot.device.aio import IoTHubDeviceClient

# function to init GPIO of the Pi
def InitGPIO():
    # print GPIO info (not needed for initialization. Just to ensure that it works)
    print(GPIO.RPI_INFO)

    # Setup GPIO mode to Broadcom
    GPIO.setmode(GPIO.BCM)

    # configure GPIO14 as input pin
    GPIO.setup(pir_port,  GPIO.IN)


async def InitIoTHubClient():
    # Fetch the connection string from an enviornment variable
    conn_str = "HostName=sameerIOTHub.azure-devices.net;DeviceId=RaspberryPi;SharedAccessKey=UBPpcMu5Hwb79ZfhnLBLz5vAF01NlndzR9OFH+/CfeA="

    # Create instance of the device client using the authentication provider
    global device_client
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()


async def main():
    # stay in the loop to monitor PIR
    try:
        while (True):
            # if the input is zero, nobody is there at the sensor
            if GPIO.input(pir_port) == 0:
                print("000")
            else:
                # found somebody at the sensor
                print("111")
                global device_client
                await device_client.send_message("Found human!")
            # wait for 1 sec whether you detect someone or not
            time.sleep(1)
    # If user presses ^C cleanup the GPIO and disconnect from the IoT Hub
    except KeyboardInterrupt:
        GPIO.cleanup()
        await device_client.disconnect()
    print("Exiting")

if __name__ == "__main__":
    InitGPIO()
    asyncio.run(InitIoTHubClient())
    asyncio.run(main())