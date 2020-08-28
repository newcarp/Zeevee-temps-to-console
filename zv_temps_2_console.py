import telnetlib
import time
import csv

def get_zyper_data():
    # your hostname or ip goes here
	Host = "192.168.11.252"

    tn = telnetlib.Telnet(Host)
    tn.read_until(b"Zyper$")

    tn.write("show device status decoders".encode('ascii') + "\n".encode('ascii'))
    time.sleep(1)

    OUTPUT = tn.read_until(b"Zyper$")
    OUTPUT = OUTPUT.decode('utf-8')

    tn.close()

    return OUTPUT

# use this def if you want to use previous output from a file for testing
def get_file_data():
    with open ('output2.txt') as data:
        file_data = data.readlines()
    return file_data

new_data = ''
zv_list_key = []
zv_temps = []
zv_units = []

#Import a list of all decoders so you can make sure you are getting data for all units
with open ('zv_names.csv', 'r') as data:
    for line in csv.reader(data):
        zv_units.append(str(line[0]))

#Get data once and get the Zeevee unit names into a list to serve as a key
zv_data = get_zyper_data().splitlines()
#zv_data = get_file_data()

# go through the data line by line and add the unit name to a list
for line in range(len(zv_data)):
    if 'model=' in zv_data[line]:
        split_line = zv_data[line].split()
        for item in range(len(split_line)):
            if 'name' in split_line[item]:
                split_line[item] = split_line[item].replace('name=', '')
                split_line[item] = split_line[item].replace(',', '')
                if len(split_line[item]) < 7:
                    split_line[item] += ' '
                new_data = split_line[item]
                zv_list_key.append(split_line[item])

zv_temps = []

# go through the data line by line and add the temp reading to a list
for line in range(len(zv_data)):
    if 'temperature' in zv_data[line]:
        zv_data[line] = zv_data[line].replace('device.temperature; main=', '')
        zv_data[line] = zv_data[line].replace('\n', '')
        zv_data[line] = zv_data[line].replace('C', '')
        new_data = new_data + zv_data[line]
        zv_data[line] = int(zv_data[line])

        zv_temps.append(zv_data[line])

# check the list of all units against the list of all the units we have readings for, if there is one that doesn't
# have a reading append it to the list with 0 for its temp reading
for line in zv_units:
    if not line in zv_list_key:
        zv_list_key.append(line)
        zv_temps.append(0)

# print the final results which can be processed by zabbix or whatever
for item in range(len(zv_list_key)):
    print (zv_list_key[item], zv_temps[item])