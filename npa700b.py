# 
#  Disclaimer
#  
#  Copyright 2018 WallyAI
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this 
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify, 
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all copies 
#  or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

def Press_2DF():

# some variable declarations
#   count_max = 14745
#   count_min = 1638

    count_max = 16380.00 # Used the old one
    count_min = 16.00
    pressure_min = -5.00  # pressure corresponding to output value 0 dec
    pressure_max = 5.00   # pressure corresponding to output value 16383 dec
    tcoeff = 2048.00     # 2^11 - see datasheet for more info

# Nova Pressure Sensor NPA 700b address, 0x28 (40)
# Read data back from 0x28(40), with offset 0, 2 bytes
# 2 bytes, Pressure LSB first

    data = bus.read_i2c_block_data(0x28, 0, 2)

# Convert to 16 bits

    pressure_raw = data[0] << 8 # High Byte, Left shift the high byte
    pressure_raw = pressure_raw + data[1]
    print "Pressure count is: %.2d" %pressure_raw
    
# calculate the slope
    slope = (count_max - count_min) / (pressure_max + abs (pressure_min)) 
 
# so final equation is = (pressure_raw * (slope)) - pressure_min
    pressure_calc = (pressure_raw / (slope)) + pressure_min
    return pressure_calc

def Press_4DF():

#   some variable declarations
#   count_max = 14745
#   count_min = 1638

#    count_max = 18000.00 # Used the old one
    count_max = 16380.00
    count_min = 16
    pressure_min = -5.00 # pressure corresponding to output value 0 dec
    pressure_max = 5.00  # pressure corresponding to output value 16383 dec
    tcoeff = 2048.00     # 2^11 see datasheet 
 
# Nova Pressure Sensor NPA 700b address, 0x28 (40)
# Read data back from 0x28(40), with offset 0, 4 bytes
# 2 bytes, Pressure LSB first

    data = bus.read_i2c_block_data(0x28, 0, 4)

# Convert to 16 bits

    pressure_raw = data[0] << 8 # High Byte, Left shift the high byte
    pressure_raw = pressure_raw + data[1]
#   print "Pressure count is: %.2d" %pressure_raw

# calculate the slope
    slope = (count_max - count_min) / (pressure_max + abs (pressure_min)) 
 
# so final equation is = (pressure_raw * (slope)) - pressure_min
    pressure_calc = (pressure_raw / (slope)) + pressure_min

# now find the temperature data

    temperature_raw = data[2] << 3 # High Byte, Left shift the high byte by 3 bits for the lower 3 bits 
    low_temp = data[3] >> 5        # Right shift it by 5 bits to put the lower 3 bits it the correct bit slot
    temperature_raw = temperature_raw + low_temp
    temperature_calc = ((temperature_raw*200.00)/tcoeff)-50.00

    return [pressure_calc, temperature_calc]

try: 

    while True:
          list_result = Press_4DF()
          print "Pressure: %3.3f psi, Temperature: %3.2f C" %(list_result[0],list_result[1]) # Read 4 Byte DF
#         print "Pressure: %3.3f " %Press_2DF() # Read 2 Byte Example           
          time.sleep(0.5)

except:
    time.sleep(0.01)

