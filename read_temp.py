"""read_temp.py

Read the temperature from a DS18B20 temperature sensor on a Raspberry Pi

This will print a Splunk-friendly key/value pair log line.
"""

__author__ = "Ed Hunsinger"
__email__ = "edrabbit@edrabbit.com"

import datetime
import glob
import os
import sys
import time

import pytz

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    (serial_num, temp_string) = lines[1].rstrip().split(' t=')
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return utc_time, serial_num, temp_c, temp_f

def print_log_line():
    utc_time, serial_num, temp_c, temp_f = read_temp()
    print ('%s serial_number="%s", temp_c=%.2f, temp_f=%.2f'
           % (utc_time, serial_num, temp_c, temp_f))


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        while True:
            print_log_line()
            time.sleep(float(sys.argv[1]))
    else:
        print_log_line()
        exit()
