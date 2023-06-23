from machine import UART, ADC
import os
import utime
import time

uart=UART(1, baudrate=115200)
temp_sensor= ADC(4)

def temperature():
    raw_sensor_data= temp_sensor.read_u16()
    sensor_voltage=(raw_sensor_data/65535)*3.3
    temperature= 27 - (sensor_voltage-0.706)/0.001721
    #print(temperature)
    return temperature

print("UART Info: ", uart)
utime.sleep(1)

while True:
    current_time= time.localtime()
    #print("the current time is: ", current_time)
    #print(current_time[5])

    date_time= str(current_time[0])+"/"+str(current_time[1])+"/"+str(current_time[2])+"***"+str(current_time[3])+":"+str(current_time[4])+":"+str(current_time[5])
        
    #print(date_time)
    temp=str(temperature())+" "+ date_time
    temp_length=len(temp)
    print(str(temp))
    #print(len(temp))
    uart.write(temp_length.to_bytes(29, 'big'))
    uart.write(str(temp))
    utime.sleep(1)
    