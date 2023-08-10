from machine import UART, ADC, Pin
import os
import utime

uart=UART(1, baudrate=115200)
temp_sensor= ADC(1)

def temperature():
    raw_sensor_data= temp_sensor.read_u16()
    sensor_voltage=(raw_sensor_data/65535)*3.3
    temperature= 27 - (sensor_voltage-0.706)/0.001721
    return raw_sensor_data

print("UART Info: ", uart)
utime.sleep(3)

while True:
    temp= int(temperature())
    print(str(temp))
    uart.write(str(temp))
    utime.sleep(1)
    