#!/usr/bin/env python3

import psutil
import math

# This script finds the average temperature across all cores

raw_temp = psutil.sensors_temperatures().get('coretemp')[1:7]

# Function to find average temp
def Average(temp):
    return sum(temp) / len(temp)

temp = []
for i in raw_temp:
    temp.append(i[1])

average_c = Average(temp)
# Convert the average Celsius to Fahrenheit
average_f = (average_c * 1.8) + 32
print(round(average_f))
