import serial
import time

from math import floor

ser= serial.Serial('/dev/ttyS0', 115200, timeout=5)
time.sleep(1)

file= open("Test_data_2.csv", "a+")

counter=0        
while True:
    #data=(ser.read(4))
    data_length_bytes= ser.read(29)
    #print(data_length_bytes)
    data_length= int.from_bytes(data_length_bytes, 'big')
    print(data_length)
    data=ser.read(data_length)
    #print(data)
    temperature= str(data, 'UTF-8')
    print(temperature)
    #counter=counter+1
    #c_o=str(counter)
    new_data= temperature 
    file.write(new_data)
    file.write("\n")
    file.flush()
    #  print(file)
    #print(new_data)
    if temperature== " ":
        print("data not fed")
    #print("Pico's Core Temperature : "+ temperature + " " + "Degree Celsius")
         