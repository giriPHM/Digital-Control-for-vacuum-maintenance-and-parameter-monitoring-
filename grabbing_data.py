import numpy as np
#import pandas as pd
import decimal
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

x_arr=[]
y_arr=[]
x_data=[]
y_data=[]
fig, ax= plt.subplots()
start_time= datetime.datetime(2023, 6, 23, 0, 0, 0)
end_time= datetime.datetime(2023, 6, 23, 23, 59, 59)
ax.set_xlim(start_time,  end_time)
ax.set_ylim(0,100)
line, =ax.plot([], [])
 
 #ax.set_xlim(0,100)
 
 
def update(data):
    x, y=data
    x_data.append(x)
    y_data.append(y)
    line.set_data(x_data, y_data)
    return line,

def init():
    line.set_data([], [])
    return line,


#print(RangeData.shape)

def generating_data():
    i=0
    while True:
        #here
        time.sleep(1)
        RangeData=np.loadtxt("Test_data_2.csv", delimiter='  ', dtype=str)
        print(RangeData[i])
        Ch0= RangeData[i].split()
        a=decimal.Decimal(Ch0[0])
        #y_arr.append(a)
        b=Ch0[1]
        
        Ch1=b.split('***')
        #print(Ch1)
        Ch2=Ch1[1].split(':')
        Ch3=Ch1[0].split('/')
        #print(Ch2[0])
        #print(Ch2[1])
        #print(Ch2[2])
        
        year, month, day=map(int, Ch1[0].split('/'))
        hour, minute, second= map(int, Ch1[1].split(':'))
        time_obj= datetime.time(hour, minute, second)
        date_obj= datetime.date(year, month, day)
        
        x=datetime.datetime.combine(date_obj, time_obj)
        
        #x_arr.append(b)
        #print(a)
        #print(b)
         #print(Ch1)
        i=i+1
        yield x, a
        #i=i+1
    '''if i==100:
        plt.plot(x_arr, y_arr)
        plt.xlabel('Date_Time')
        plt.ylabel('Temperature')
        plt.title('Graph of temperature over time')
        plt.savefig('/home/pi/images/image'+' '+str(i))
        x_arr.clear()
        y_arr.clear()   
    time.sleep(1)'''
ani= animation.FuncAnimation(fig, update, generating_data, init_func=init, blit=True, interval=100)
plt.show()
